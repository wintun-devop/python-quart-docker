from quart import jsonify,make_response,Blueprint,request
from pydantic import ValidationError

#import bcrypt
from server import bcrypt


#jwt function import
from quart_jwt_extended import (
                                jwt_required,
                                set_access_cookies,
                                set_refresh_cookies,
                                create_access_token,
                                create_refresh_token,
                                unset_jwt_cookies,
                                jwt_refresh_token_required,
                                get_jwt_identity
                                )

from server.resources.api_paths import USER_REGISER
from server.schema.users_schema import UserCreate,UserRead,UserUpdate

#declare blue print
register_bp = Blueprint('register',__name__,url_prefix=USER_REGISER)
@register_bp.route("/",methods=['POST'])
async def create_user():
    try:
        req_body = await request.get_json()
        validate_body = UserCreate.model_validate(req_body)
        validate_values = validate_body.model_dump()
        email = validate_values["email"]
        password = validate_values["password"]
        hash_password = bcrypt.generate_password_hash(password).decode("utf-8")
        return await make_response(jsonify({"pass":hash_password}),201)
    except ValidationError as e:
        return await make_response(jsonify({"error": e.errors()}), 400)
    except Exception as e:
        print("eee",e)
        # db_session.rollback()
        error = {"status": "fail", "msg": "An unexpected error occurred"}
        return await make_response(jsonify(error), 500)



