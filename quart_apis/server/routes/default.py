from quart import Blueprint,jsonify,make_response


servertest_bp = Blueprint('test',__name__)

@servertest_bp.route('/',methods=['GET'])
async def index():
    response = {
        "status":"success",
        "message":"api is working ok!"
    }
    return await make_response(jsonify(response))