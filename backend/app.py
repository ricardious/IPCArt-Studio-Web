from flask import Flask
from routes.auth_routes import auth_router
from routes.admin_routes import admin_router
from routes.user_routes import user_router
from routes.image_routes import image_router
from routes.statistics_routes import statistics_router

app = Flask(__name__)

# Registrar los Blueprints
app.register_blueprint(auth_router, url_prefix="/auth")
app.register_blueprint(admin_router, url_prefix="/admin")
app.register_blueprint(user_router, url_prefix="/user")
app.register_blueprint(image_router, url_prefix="/image")
app.register_blueprint(statistics_router, url_prefix="/statistics")


# Función para listar todas las rutas
# def list_routes(app):
#     routes = []
#     for rule in app.url_map.iter_rules():
#         routes.append(
#             {"endpoint": rule.endpoint, "methods": list(rule.methods), "url": rule.rule}
#         )
#     return routes


if __name__ == "__main__":
    # Listar todas las rutas antes de ejecutar el servidor

    # for route in list_routes(app):
    # print(

    # f"Endpoint: {route['endpoint']}, Methods: {', '.join(route['methods'])}, URL: {route['url']}"

    # )

    app.run(host="0.0.0.0", port=4000, debug=True)
