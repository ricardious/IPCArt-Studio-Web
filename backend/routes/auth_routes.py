import os
from flask import Blueprint, request, jsonify
from services.auth_service import AuthService
from services.user_service import UsersService


users_service = UsersService()

# XML file configuration and AuthService
auth_service = AuthService(users_service)

# Blueprint for authentication routes
auth_router = Blueprint("auth", __name__)


@auth_router.route("/login", methods=["POST"])
def login():
    """
    Login endpoint.
    Expects a JSON with 'username' and 'password'.
    Returns a success or error message based on authentication.
    """
    try:
        # Get data from request body
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

        # Authentication logic
        response = auth_service.login(username, password)
        if response["status"] == "success":
            return jsonify(response), 200
        else:
            return jsonify(response), 401
    except Exception as e:
        # General error handling
        return (
            jsonify({"status": "error", "message": f"Internal Server Error: {str(e)}"}),
            500,
        )
