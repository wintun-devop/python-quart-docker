from quart import jsonify,make_response,request,Blueprint
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
import uuid
from pydantic import ValidationError



from server.models.db import get_write_session
from server.models.db import get_read_session
from server.schema.items_schema import InventoryCreate,InventoryRead,InventoryUpdate

from server.services.products_services import (
                                               item_create,
                                               item_get_all,
                                               item_get_one,
                                               item_update,
                                               item_delete
                                               )
from server.server_config import server_path
from server.utils.unique_string import unique_string


from server.resources.api_paths import ITEMS_API_PATH
items_bp = Blueprint('items',__name__,url_prefix=ITEMS_API_PATH)

@items_bp.route("/",methods=['POST'])
async def create_item():
    try:
        req_body = await request.get_json()
        validate_body = InventoryCreate.model_validate(req_body)
        data = {**validate_body.model_dump(),"id":str(uuid.uuid4())}
        async for session in get_write_session():
            item = await item_create(session, data)
            return await make_response(jsonify(InventoryRead.model_validate(item).model_dump(mode="json")), 201)
    except IntegrityError as e:
        print("e",e)
        session.rollback()
        error = {"status": "error", "message": "Product already exist."}
        return await make_response(jsonify(error), 400) 
    except SQLAlchemyError as e:
        print("ee",e)
        session.rollback()
        error={"status":"fail","message":"internal server error"}
        return await make_response(jsonify(error), 500)
    except ValidationError as e:
        return await make_response(jsonify({"error": e.errors()}), 400)
    except Exception as e:
        print("eee",e)
        # db_session.rollback()
        error = {"status": "fail", "message": "An unexpected error occurred"}
        return await make_response(jsonify(error), 500)
    

@items_bp.route('/<id>',methods=["GET"])
async def get_item(id):
    try:
        async for session in get_read_session():
            item = await item_get_one(session,id)
            if not item:
                return await make_response(jsonify({"error": "Item not found"}), 404)
            return await make_response(jsonify(InventoryRead.model_validate(item).model_dump(mode="json")), 200)
    except Exception as e:
        print("eee",e)
        # db_session.rollback()
        error = {"status": "fail", "message": "An unexpected error occurred"}
        return await make_response(jsonify(error), 500)
    

@items_bp.route('/<id>',methods=["PUT"])
async def update_item(id):
    try:
        req_body = await request.get_json()
        validated = InventoryUpdate.model_validate(req_body)
        async for session in get_write_session():
            updated = await item_update(session, id, validated.model_dump(exclude_unset=True))
            if not updated:
                return await make_response(jsonify({"error": "Item not found"}), 404)
            return await make_response(jsonify(InventoryRead.model_validate(updated).model_dump(mode="json")), 200)
    except ValidationError as e:
        return await make_response(jsonify({"error": e.errors()}), 400)
    except Exception as e:
        print("eee",e)
        # db_session.rollback()
        error = {"status": "fail", "message": "An unexpected error occurred"}
        return await make_response(jsonify(error), 500)
    

@items_bp.route('/<id>',methods=["DELETE"])
async def delete_item(id):
    try:
        async for session in get_write_session():
            success = await item_delete(session, id)
            if not success:
                return await make_response(jsonify({"error": "Item not found"}), 404)
            return await make_response("", 204)
    except Exception as e:
        print("eee",e)
        error = {"status": "fail", "message": "An unexpected error occurred"}
        return await make_response(jsonify(error), 500)
    

@items_bp.route('/',methods=["GET"])
async def get_all_items():
    try:
        async for session in get_read_session():
            items = await item_get_all(session)
            response = [InventoryRead.model_validate(item).model_dump(mode="json") for item in items]
            return await make_response(jsonify(response), 200)
    except Exception as e:
        print("eee",e)
        error = {"status": "fail", "message": "An unexpected error occurred"}
        return await make_response(jsonify(error), 500)


@items_bp.route("/upload",methods=['POST'])
async def upload_product():
    try:
        file = (await request.files).get("image")  
        if file and file.filename:
            # Check file type
            if file.content_type not in ["image/jpeg", "image/png","image/jpg"]:
                return {"error": "Unsupported file type"}, 400
            # Save or process the image
            suffix = (file.content_type).split("/")[-1]
            current_path =server_path    
            file_name = f"{unique_string("item_",20)}.{suffix}"
            save_path = f"{current_path}/statics/{file_name}"
            await file.save(str(save_path))
        return await make_response(jsonify({"statu":"success","file_name":file_name}), 200)
    except Exception as e:
        print("error",e)
        error = {"status": "fail", "message": "An unexpected error occurred"}
        return await make_response(jsonify(error), 500)


