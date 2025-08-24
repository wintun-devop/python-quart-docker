from server import app_instance

# #import blue print
# from server.routes.default import servertest_bp
# from server.routes.app.inventories.items import items_bp

#create instance
app = app_instance()

# #blueprint register here
# app.register_blueprint(servertest_bp)
# app.register_blueprint(items_bp)

if __name__ == "__main__":
    app.run()