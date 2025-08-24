#to creat app instance
from quart import Quart
#cors setting
from quart_cors import cors
#authentication and authorization for jwt
from quart_jwt_extended import JWTManager
from datetime import timedelta
#bcrypt for password hashing
from quart_bcrypt import Bcrypt
#import server configurations
from . import server_config


#declare bcrypt global instance
bcrypt = Bcrypt()


def app_instance():
    app = Quart(__name__)
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
    # Enable csrf double submit protection. See this for a thorough
    # explanation: http://www.redotheweb.com/2015/11/09/api-security.html
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    JWTManager(app)
    #database config
    #bcrypt hasing
    bcrypt.init_app(app)
    return app