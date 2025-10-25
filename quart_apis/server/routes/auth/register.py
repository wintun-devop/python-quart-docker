import uuid
from quart import jsonify,make_response,Blueprint,request
from pydantic import ValidationError
from quart_schema import validate_request, validate_response
from sqlalchemy.exc import IntegrityError
import asyncpg

# from server.utils.hash import hash_password
from server.utils.argon2_hash import hash_password_argon2
from server.models.db import get_write_session
from server.utils.unique_string import unique_string
from server.resources.api_paths import USER_REGISER
from server.schema.users_schema import UserCreate,UserCustomRead
from server.services.users_services import user_create


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


#declare blue print
register_bp = Blueprint('register',__name__,url_prefix=USER_REGISER)
@register_bp.route("/",methods=['POST'])
@validate_request(UserCreate)
@validate_response(UserCustomRead,201)
async def create_user(data:UserCreate):
    try:
        hash_pass =await hash_password_argon2(data.password)
        payload = {
            "id":str(uuid.uuid4()),
            "email":data.email,
            "password":hash_pass,
            "username":unique_string("usr")
        }
        async for session in get_write_session():
            user = await user_create(session, payload)
            resp = UserCustomRead.model_validate(user).model_dump(mode="json")
            return resp, 201
    except IntegrityError as err:
            print("un",err)
            return {"status": "fail","msg": "unique constraint"}, 400
    except Exception as e:
        print("eee",e)
        # db_session.rollback()
        error = {"status": "fail", "msg": "An unexpected error occurred"}
        return error, 500


