import xml.etree.ElementTree as ET
import os
from xml.dom import minidom
from models.user import User


class UsersService:
    """
    A service for managing user data stored in an XML file.
    Handles operations such as adding, updating, deleting, and retrieving users.
    """

    def __init__(self):
        """Initialize Users Service with storage paths."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        self.storage_path = os.path.join(project_root, "database")
        self.storage_path = os.path.abspath(self.storage_path)
        self.users_file = os.path.join(self.storage_path, "usuarios.xml")

        # Create storage directory if it doesn't exist
        os.makedirs(self.storage_path, exist_ok=True)

        # Initialize XML files if they don't exist
        self._initialize_users_file()

    def _initialize_users_file(self):
        """Initialize the users XML file if it doesn't exist."""
        if not os.path.exists(self.users_file):
            root = ET.Element("usuarios")
            tree = ET.ElementTree(root)
            self._write_pretty_xml(tree)

    def _write_pretty_xml(self, tree):
        """Write XML with proper formatting."""
        try:
            xmlstr = minidom.parseString(ET.tostring(tree.getroot())).toprettyxml(
                indent="\t"
            )
            xmlstr = "\n".join([line for line in xmlstr.splitlines() if line.strip()])
            with open(self.users_file, "w", encoding="utf-8") as f:
                f.write(xmlstr)
        except (ET.ParseError, IOError) as e:
            raise Exception(f"Error writing XML: {e}")

    def save_users(self, users):
        """
        Save a list of User objects to the XML file.
        Args:
            users (list[User]): List of User objects to save.
        """
        try:
            self._initialize_users_file()
            tree = ET.parse(self.users_file)
            root = tree.getroot()

            for user in users:
                if self._user_exists(user.user_id, root):
                    continue  # Skip duplicate users

                user_elem = ET.SubElement(
                    root, "usuario", {"id": user.user_id, "pwd": user.pwd}
                )
                ET.SubElement(user_elem, "NombreCompleto").text = user.full_name
                ET.SubElement(user_elem, "CorreoElectronico").text = user.email
                ET.SubElement(user_elem, "NumeroTelefono").text = user.phone_number
                ET.SubElement(user_elem, "Direccion").text = user.address
                ET.SubElement(user_elem, "Perfil").text = user.profile_url

            self._write_pretty_xml(tree)

        except Exception as e:
            raise Exception(f"Error saving users: {e}")

    def get_users(self):
        """
        Retrieve all users from the XML file.
        Returns:
            list[User]: List of User objects.
        """
        try:
            tree = ET.parse(self.users_file)
            root = tree.getroot()

            users = []
            for user_elem in root.findall("usuario"):
                user = User(
                    user_id=user_elem.get("id"),
                    pwd=user_elem.get("pwd"),
                    full_name=user_elem.find("NombreCompleto").text or "",
                    email=user_elem.find("CorreoElectronico").text or "",
                    phone_number=user_elem.find("NumeroTelefono").text or "",
                    address=user_elem.find("Direccion").text or "",
                    profile_url=user_elem.find("Perfil").text or "",
                )
                users.append(user)

            return users

        except Exception as e:
            raise Exception(f"Error retrieving users: {e}")

    def get_user_by_id(self, username):
        """
        Retrieve a user by their username from the XML file.
        Args:
            username (str): The username of the user to retrieve.
        Returns:
            User: The user object if found, otherwise None.
        """
        try:
            tree = ET.parse(self.users_file)
            root = tree.getroot()

            # Find user by username
            user_elem = root.find(f"./usuario[@id='{username}']")
            if user_elem is not None:
                return User(
                    user_id=user_elem.get("id"),
                    pwd=user_elem.get("pwd"),
                    full_name=user_elem.find("NombreCompleto").text or "",
                    email=user_elem.find("CorreoElectronico").text or "",
                    phone_number=user_elem.find("NumeroTelefono").text or "",
                    address=user_elem.find("Direccion").text or "",
                    profile_url=user_elem.find("Perfil").text or "",
                )
            return None

        except Exception as e:
            raise Exception(f"Error retrieving user by username: {e}")

    def get_user_dict(self, user_id):
        """
        Returns a dictionary with the user data given their ID.
        Args:
            user_id (str): The user ID.
        Returns:
            dict: Dictionary with user data if exists, otherwise None.
        """
        try:
            user = self.get_user_by_id(user_id)  # Use existing function
            if user:
                return {
                    "id": user.user_id,
                    "NombreCompleto": user.full_name,
                    "CorreoElectronico": user.email,
                    "NumeroTelefono": user.phone_number,
                    "Direccion": user.address,
                    "Perfil": user.profile_url,
                }
            return None
        except Exception as e:
            raise Exception(f"Error generating user dictionary: {e}")

    def add_user(self, user):
        """
        Add a single user to the XML file.
        Args:
            user (User): User object to add.
        Returns:
            bool: True if successful, False if user already exists.
        """
        try:
            tree = ET.parse(self.users_file)
            root = tree.getroot()

            if self._user_exists(user.user_id, root):
                return False

            user_elem = ET.SubElement(
                root, "usuario", {"id": user.user_id, "pwd": user.pwd}
            )
            ET.SubElement(user_elem, "NombreCompleto").text = user.full_name
            ET.SubElement(user_elem, "CorreoElectronico").text = user.email
            ET.SubElement(user_elem, "NumeroTelefono").text = user.phone_number
            ET.SubElement(user_elem, "Direccion").text = user.address
            ET.SubElement(user_elem, "Perfil").text = user.profile_url

            self._write_pretty_xml(tree)
            return True

        except Exception as e:
            raise Exception(f"Error adding user: {e}")

    def _user_exists(self, user_id, root):
        """Check if a user with the given ID already exists."""
        return root.find(f"./usuario[@id='{user_id}']") is not None
