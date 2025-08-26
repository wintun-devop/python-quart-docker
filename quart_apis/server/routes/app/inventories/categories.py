from quart import jsonify,make_response,request,Blueprint
from server.resources.api_paths import CATEGORIES_API_PATH

categories_bp = Blueprint('categories',__name__,url_prefix=CATEGORIES_API_PATH)

@categories_bp.route("/",methods=['POST'])
async def create_category():
    try:
        req_body = await request.get_json()
        response = dict(req_body)
        return await make_response(jsonify(response),201)
    # except IntegrityError as e:
    #     print("e",e)
    #     # db_session.rollback()
    #     error = {"status": "fail", "message": "Product already exist."}
    #     return await make_response(jsonify(error), 400) 
    # except SQLAlchemyError as e:
    #     print("ee",e)
    #     db_session.rollback()
    #     error={"status":"fail","message":"internal server error"}
    #     return await make_response(jsonify(error), 500)
    except Exception as e:
        print("eee",e)
        # db_session.rollback()
        error = {"status": "fail", "message": "An unexpected error occurred"}
        return await make_response(jsonify(error), 500)
    


@categories_bp.route('/<id>',methods=["GET"])
async def get_category(id):
    try:
        # product = db_read_session.query(Products).filter_by(id=id).first()
        # if product is None:
        #     return make_response(jsonify({"status": "fail", "msg": "Product not found"}), 404)
        response = {
            "id": id,
        }
        return await make_response(jsonify(response), 200)
    # except exc.SQLAlchemyError as e:
    #     print("error", e)
    #     return make_response(jsonify({"status": "failed", "msg": "Internal Server Error"}), 500)
    except Exception as e:
        print("eee",e)
        # db_session.rollback()
        error = {"status": "fail", "message": "An unexpected error occurred"}
        return await make_response(jsonify(error), 500)
    

@categories_bp.route('/<id>',methods=["PUT"])
async def update_category(id):
    try:
        # product = db_read_session.query(Products).filter_by(id=id).first()
        # if product is None:
        #     return make_response(jsonify({"status": "fail", "msg": "Product not found"}), 404)
        response = {
            "id": id,
        }
        return await make_response(jsonify(response), 200)
    # except exc.SQLAlchemyError as e:
    #     print("error", e)
    #     return make_response(jsonify({"status": "failed", "msg": "Internal Server Error"}), 500)
    except Exception as e:
        print("eee",e)
        # db_session.rollback()
        error = {"status": "fail", "message": "An unexpected error occurred"}
        return await make_response(jsonify(error), 500)
    

@categories_bp.route('/<id>',methods=["DELETE"])
async def delete_category(id):
    try:
        # product = db_read_session.query(Products).filter_by(id=id).first()
        # if product is None:
        #     return make_response(jsonify({"status": "fail", "msg": "Product not found"}), 404)
        response = {
            "id": id,
        }
        return await make_response(jsonify(response), 200)
    # except exc.SQLAlchemyError as e:
    #     print("error", e)
    #     return make_response(jsonify({"status": "failed", "msg": "Internal Server Error"}), 500)
    except Exception as e:
        print("eee",e)
        # db_session.rollback()
        error = {"status": "fail", "message": "An unexpected error occurred"}
        return await make_response(jsonify(error), 500)
    

@categories_bp.route('/',methods=["GET"])
async def get_all_categories():
    try:
        # product = db_read_session.query(Products).filter_by(id=id).first()
        # if product is None:
        #     return make_response(jsonify({"status": "fail", "msg": "Product not found"}), 404)
        response = []
        return await make_response(jsonify(response), 200)
    # except exc.SQLAlchemyError as e:
    #     print("error", e)
    #     return make_response(jsonify({"status": "failed", "msg": "Internal Server Error"}), 500)
    except Exception as e:
        print("eee",e)
        # db_session.rollback()
        error = {"status": "fail", "message": "An unexpected error occurred"}
        return await make_response(jsonify(error), 500)