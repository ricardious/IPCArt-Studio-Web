from xml.etree import ElementTree as ET
from utils.validators import validate_user_id, validate_email, validate_phone
from models.user import User
from models.image import Image
from models.pixel import Pixel


def parse_users(xml_content):
    """
    Parse and validate users from XML content.
    Args:
        xml_content (str): Raw XML content.
    Returns:
        list[User]: List of valid User objects.
    """
    try:
        root = ET.fromstring(xml_content)
        users = []

        for user_elem in root.findall("solicitante"):

            user = User(
                user_id=user_elem.get("id"),
                pwd=user_elem.get("pwd"),
                full_name=user_elem.find("NombreCompleto").text or "",
                email=user_elem.find("CorreoElectronico").text or "",
                phone_number=user_elem.find("NumeroTelefono").text or "",
                address=user_elem.find("Direccion").text or "",
                profile_url=user_elem.find("perfil").text or "",
            )

            if (
                validate_user_id(user.user_id)
                and user.pwd
                and validate_email(user.email)
                and validate_phone(user.phone_number)
            ):
                users.append(user)

        return users

    except ET.ParseError:
        raise ValueError("Invalid XML format")


def parse_image(xml_content, user_id):
    """
    Parse the XML content to create an Image object.

    Args:
        xml_content (bytes): The raw XML content.
        user_id (str): The ID of the user associated with the image.

    Returns:
        Image: An Image object parsed from the XML.

    Raises:
        ValueError: If the XML structure is invalid or contains missing data.
    """
    try:
        tree = ET.ElementTree(ET.fromstring(xml_content))
        root = tree.getroot()

        if root.tag != "figura":
            raise ValueError("Invalid XML structure: Root tag must be 'figura'.")

        name_elem = root.find("nombre")
        if name_elem is None or not name_elem.text:
            raise ValueError("Missing or invalid 'nombre' tag.")

        image_name = name_elem.text

        design_elem = root.find("diseño")
        if design_elem is None:
            raise ValueError("Missing 'diseño' tag.")

        pixels = []
        for pixel_elem in design_elem.findall("pixel"):
            try:
                row = int(pixel_elem.get("fila"))
                col = int(pixel_elem.get("col"))
                color = pixel_elem.text
                if not color:
                    raise ValueError("Pixel color is missing.")
                pixels.append(Pixel(row=row, column=col, color=color))
            except (ValueError, TypeError) as e:
                raise ValueError(f"Invalid pixel data: {e}")

        return Image(
            id=None,
            user_id=user_id,
            name=image_name,
            pixels=pixels,
        )

    except ET.ParseError as e:
        raise ValueError(f"Invalid XML format: {e}")
