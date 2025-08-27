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

from server.resources.api_paths import USER_LOGIN

from server.schema.users_schema import UserCreate,UserRead,UserUpdate


#declare blue print
login_bp = Blueprint('login',__name__,url_prefix=USER_LOGIN)
@login_bp.route("/",methods=['POST'])
async def login():
    try:
        req_body = await request.get_json()
        validate_body = UserCreate.model_validate(req_body)
        validate_values = validate_body.model_dump()
        email = validate_values["email"]
        password = validate_values["password"]
        return await make_response(jsonify({}),200)
    except ValidationError as e:
        return await make_response(jsonify({"error": e.errors()}), 400)
    except Exception as e:
        print("eee",e)
        # db_session.rollback()
        error = {"status": "fail", "msg": "An unexpected error occurred"}
        return await make_response(jsonify(error), 500)