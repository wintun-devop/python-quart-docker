#to creat app instance
from quart import Quart,jsonify
#cors setting
from quart_cors import cors
#authentication and authorization for jwt
from quart_jwt_extended import JWTManager
from datetime import timedelta
#bcrypt for password hashing
from quart_bcrypt import Bcrypt
#swgger docs
from quart_schema import QuartSchema,Info,RequestSchemaValidationError, ResponseSchemaValidationError
from werkzeug.exceptions import BadRequest

#import server configurations
from . import server_config


#declare bcrypt global instance
bcrypt = Bcrypt()

#import blue prints
from server.routes.default import servertest_bp
from server.routes.app.inventories import (items_bp,categories_bp)
from server.routes.auth import (register_bp,login_bp,logout_bp)


# List of blueprints
blue_prints = [
               servertest_bp, 
               items_bp, 
               categories_bp,
               register_bp,
               login_bp,
               logout_bp
               ]


def app_instance():
    app = Quart(__name__)
    QuartSchema(app,info=Info(
            title="Quart API Server",
            version="1.0.0",
            description="Quart API Server with custom version."
    ))
    #quart schema error handling 
    @app.errorhandler(RequestSchemaValidationError)
    async def handle_request_validation_error(error):
        # error.validation_error is a Pydantic ValidationError (or msgspec/TypeError)
        ve = getattr(error, "validation_error", None)
        if ve is not None:
            # Pydantic ValidationError has .errors()
            try:
                return jsonify({"status":"error","msg":"validation_failed", "detail": ve.errors()}), 400
            except Exception:
                return jsonify({"error": "validation_failed", "detail": str(ve)}), 400
        return jsonify({"error": "bad request", "detail": str(error)}), 400
    @app.errorhandler(BadRequest)
    async def handle_bad_request(err):
        # err.description may include parser details; avoid leaking internals in production
        return jsonify({"error": "bad request", "detail": str(err.description)}), 400
    app.config['SECRET_KEY']=server_config.APP_SECRET_KEY
    #configure cors
    app = cors(app, allow_origin="*")
    #configure jwt
    # Configure application to store JWTs in cookies
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    # Only allow JWT cookies to be sent over https. In production, this
    # should likely be True
    app.config["JWT_COOKIE_SECURE"] = False
    app.config['JWT_SECRET_KEY'] = server_config.JWT_SECRET_KEY
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=10)  # Adjust as needed
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=10)  # Adjust as needed
    app.config['JWT_REFRESH_TOKEN_ENABLED'] = True
    app.config['JWT_TOKEN_LOCATION'] = ["cookies"]
    app.config['JWT_COOKIE_SECURE'] = True
    # Enable csrf double submit protection. See this for a thorough
    # explanation: http://www.redotheweb.com/2015/11/09/api-security.html
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    JWTManager(app)
    """ register blueprint """
    for blue_print in blue_prints:
        app.register_blueprint(blue_print)
    return app


