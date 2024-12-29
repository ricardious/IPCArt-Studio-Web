class AuthService:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        # Credenciales fijas para el administrador
        self.admin_credentials = {
            "username": "AdminIPC",
            "password": "ARTIPC2",
        }

    def login(self, username, password):
        # Validar credenciales del administrador
        if (
            username == self.admin_credentials["username"]
            and password == self.admin_credentials["password"]
        ):
            return {
                "status": "success",
                "message": f"Welcome Admin!",
                "role": "admin",
            }

        # Validar credenciales de usuarios en el archivo XML
        user = self.db_manager.get_user(username)
        if user and user.pwd == password:
            return {
                "status": "success",
                "message": f"Welcome {user.full_name}!",
                "role": "user",
            }
        return {"status": "error", "message": "Invalid username or password."}
