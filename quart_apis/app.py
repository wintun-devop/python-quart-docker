from server import app_instance
#import blue print
from server.routes.default import servertest_bp

#create instance
app = app_instance()

#blueprint register here
app.register_blueprint(servertest_bp)

if __name__ == "__main__":
    app.run()