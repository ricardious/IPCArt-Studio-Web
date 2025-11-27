from flask import Flask, jsonify
from routes.auth_routes import auth_router
from routes.admin_routes import admin_router
from routes.user_routes import user_router
from routes.image_routes import image_router
from routes.statistics_routes import statistics_router

app = Flask(__name__)

app.register_blueprint(auth_router, url_prefix="/auth")
app.register_blueprint(admin_router, url_prefix="/admin")
app.register_blueprint(user_router, url_prefix="/user")
app.register_blueprint(image_router, url_prefix="/image")
app.register_blueprint(statistics_router, url_prefix="/statistics")


@app.route("/")
def index():
    return jsonify(
        {
            "message": "IPCArt-Studio Web API running successfully 🚀",
            "base_endpoints": {
                "auth": "/auth",
                "admin": "/admin",
                "user": "/user",
                "image": "/image",
                "statistics": "/statistics",
            },
        }
    )


@app.route("/ping")
def ping():
    return "pong", 200


if __name__ == "__main__":
    app.run(debug=True, port=4000)
