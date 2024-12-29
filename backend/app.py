from flask import Flask
from routes.auth_routes import auth_router

app = Flask(__name__)

# Registrar el Blueprint de autenticación
app.register_blueprint(auth_router, url_prefix="/auth")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)
