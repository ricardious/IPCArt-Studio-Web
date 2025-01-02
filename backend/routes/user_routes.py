from flask import Blueprint, request, jsonify
from services.user_service import UsersService


user_router = Blueprint("user", __name__)
users_service = UsersService()


@user_router.route("/<user_id>", methods=["GET"])
def get_user_by_id(user_id):
    try:
        user = users_service.get_user_by_id(user_id)

        if user:
            user_data = {
                "user_id": user.user_id,
                "full_name": user.full_name,
                "email": user.email,
                "phone_number": user.phone_number,
                "address": user.address,
                "profile_url": user.profile_url,
            }
            return jsonify({"status": "success", "data": user_data}), 200
        else:
            return jsonify({"status": "error", "message": "User not found"}), 404
    except Exception as e:
        return (
            jsonify({"status": "error", "message": f"Internal Server Error: {str(e)}"}),
            500,
        )
