import os
from models.user import User
import xml.etree.ElementTree as ET


class DBManager:
    def __init__(self, file_path):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            self._initialize_file()

    def _initialize_file(self):
        root = ET.Element("usuarios")
        tree = ET.ElementTree(root)
        tree.write(self.file_path)

    def get_user(self, user_id):
        """
        Busca un usuario por su ID en el archivo XML.
        :param user_id: ID del usuario que se desea buscar.
        :return: Una instancia de User si el usuario existe, None en caso contrario.
        """
        tree = ET.parse(self.file_path)
        root = tree.getroot()

        for usuario in root.findall("usuario"):
            if usuario.get("id") == user_id:  # Buscar por atributo 'id'
                return User(
                    user_id=usuario.get("id"),
                    pwd=usuario.get("pwd"),
                    full_name=usuario.find("NombreCompleto").text,
                    email=usuario.find("CorreoElectronico").text,
                    phone_number=usuario.find("NumeroTelefono").text,
                    address=usuario.find("Direccion").text,
                    profile_url=usuario.find("perfil").text,
                )
        return None
