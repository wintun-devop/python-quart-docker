import uuid
from quart import jsonify,make_response,Blueprint,request
from pydantic import ValidationError



from server.utils.hash import hash_password
from server.models.db import get_write_session
from server.utils.unique_string import unique_string
from server.resources.api_paths import USER_REGISER
from server.schema.users_schema import UserCreate,UserRead,UserUpdate,UserCustomRead
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
async def create_user():
    try:
        req_body = await request.get_json()
        validate_body = UserCreate.model_validate(req_body)
        validate_values = validate_body.model_dump()
        # hash_pass =await hash_password(validate_values["password"])
        data = {
            "id":str(uuid.uuid4()),
            "email":validate_values["email"],
            "password":hash_password(validate_values["password"]),
            "username":unique_string("usr")
        }
        async for session in get_write_session():
            user = await user_create(session, data)
            return await make_response(jsonify(UserCustomRead.model_validate(user).model_dump(mode="json")), 201)
    except ValidationError as e:
        return await make_response(jsonify({"error": e.errors()}), 400)
    except Exception as e:
        print("eee",e)
        # db_session.rollback()
        error = {"status": "fail", "msg": "An unexpected error occurred"}
        return await make_response(jsonify(error), 500)



