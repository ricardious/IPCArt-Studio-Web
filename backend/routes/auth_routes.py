import os
from flask import Blueprint, request, jsonify
from services.auth_service import AuthService
from database.db_manager import DBManager

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(os.path.dirname(current_dir), "database", "users.xml")

# Configuración del archivo XML y AuthService
db_manager = DBManager(db_path)
auth_service = AuthService(db_manager)

# Crear un Blueprint para las rutas de autenticación
auth_router = Blueprint("auth", __name__)


@auth_router.route("/login", methods=["POST"])
def login():
    """
    Endpoint para iniciar sesión.
    Espera un JSON con 'username' y 'password'.
    Devuelve un mensaje de éxito o error según la autenticación.
    """
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.get_json()
        if not data or "username" not in data or "password" not in data:
            return (
                jsonify(
                    {"status": "error", "message": "Missing username or password."}
                ),
                400,
            )

        username = data["username"]
        password = data["password"]

        # Lógica de autenticación
        response = auth_service.login(username, password)
        if response["status"] == "success":
            return jsonify(response), 200
        else:
            return jsonify(response), 401
    except Exception as e:
        # Manejo de errores generales
        return (
            jsonify({"status": "error", "message": f"Internal Server Error: {str(e)}"}),
            500,
        )
