from quart import jsonify,make_response,Blueprint,request
from pydantic import ValidationError
from quart_schema import validate_request, validate_response


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
from server.models.db import get_read_session
from server.services.users_services import user_get_by_email,user_get_one
# from server.utils.hash import check_password
from server.utils.argon2_hash import verify_password_argon2


#declare blue print
login_bp = Blueprint('login',__name__,url_prefix=USER_LOGIN)
@login_bp.route("/",methods=['POST'])
@validate_request(UserCreate)
# @validate_response(UserCustomRead,201)
async def login(data:UserCreate):
    try:
        async for session in get_read_session():
            user = await user_get_by_email(session,data.email)
            if not user:
                return jsonify({"error": "user or password incorrect."}), 400
            token_attribute = { 
                "id":user.id,
                "username":user.username
                }
            hash_password = user.password
            print("hash",hash_password)
            vertify_password = await verify_password_argon2(hash_password,data.password)
            if not vertify_password["ok"]:
                return jsonify({"error": "user or password incorrect."}), 400
            access_token = create_access_token(identity=token_attribute,fresh=True)
            refresh_token = create_refresh_token(identity=token_attribute)
            resp = await make_response(jsonify({
                **token_attribute,
                "access_token": access_token,
                "refresh_token": refresh_token,
                "auth":True
            }), 200)
            # Important: pass the Response object as the first arg
            set_access_cookies(resp, access_token)
            set_refresh_cookies(resp, refresh_token)
            return resp
    except Exception as e:
        print("eee",e)
        error = {"status": "fail", "msg": "An unexpected error occurred"}
        return await make_response(jsonify(error), 500)