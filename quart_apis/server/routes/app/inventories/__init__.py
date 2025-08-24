from quart import Blueprint
from server.resources.api_paths import ITEMS_API_PATH
from server.resources.api_paths import CATEGORIES_API_PATH

#declare blue print in organize way
items_bp = Blueprint('items',__name__,url_prefix=ITEMS_API_PATH)
categories_bp = Blueprint('categories',__name__,url_prefix=CATEGORIES_API_PATH)