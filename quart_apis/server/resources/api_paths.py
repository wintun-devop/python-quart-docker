from server.server_config import api_base_path


# base_path="/api/v1"
base_path=api_base_path

#api end-points
AUTH_API_LINK_TEST =f"{base_path}/auth/test"
AUTHORIZED_TEST =f"{base_path}/test-authorize"
USER_REGISER=f"{base_path}/auth/register"
USER_LOGIN=f"{base_path}/auth/login"
USER_LOGOUT=f"{base_path}/auth/logout"
REFRESH_TOKEN=f"{base_path}/auth/refresh"
USERS=f"{base_path}/users"
USER=f"{base_path}/user"

#Authorized
PRODUCT_API_PATH=f"{base_path}/product"
ITEMS_API_PATH=f"{base_path}/items"
CATEGORIES_API_PATH=f"{base_path}/categories"