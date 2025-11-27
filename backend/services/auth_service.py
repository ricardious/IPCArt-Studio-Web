from services.user_service import UsersService


class AuthService:
    def __init__(self, users_service: UsersService | None = None):
        self.users_service = users_service or UsersService()

        # Fixed admin credentials
        self.admin_credentials = {
            "username": "AdminIPC",
            "password": "ARTIPC2",
        }

    def login(self, username: str, password: str) -> dict:
        # Validate admin credentials
        if (
            username == self.admin_credentials["username"]
            and password == self.admin_credentials["password"]
        ):
            return {
                "status": "success",
                "message": f"Welcome Admin!",
                "role": "admin",
                "user_id": "admin",
            }

        user = self.users_service.get_user_by_id(username)
        # Validate user credentials
        if user and user.pwd == password:
            return {
                "status": "success",
                "message": f"Welcome {user.full_name}!",
                "role": "user",
                "user_id": user.user_id,
            }
        return {"status": "error", "message": "Invalid username or password."}
