from flask import Blueprint, request, jsonify, Response
from xml.etree import ElementTree as ET
from xml.dom import minidom
from services.user_service import UsersService
from services.image_service import ImageService
from utils.xml_parser import parse_users
from models.user import User
from xml.sax.saxutils import escape
import traceback

admin_router = Blueprint("admin", __name__)
users_service = UsersService()
image_service = ImageService()


@admin_router.route("/bulk-upload", methods=["POST"])
def upload_users():
    """
    Upload users in bulk from an XML file.
    """
    try:
        if "file" not in request.files:
            return jsonify({"status": "error", "message": "No file provided"}), 400

        file = request.files["file"]
        print(file)
        if file.filename == "":
            return jsonify({"status": "error", "message": "No file selected"}), 400

        if not file.filename.endswith(".xml"):
            return jsonify({"status": "error", "message": "Invalid file format"}), 400

        xml_content = file.read().decode("utf-8")
        print(xml_content)
        users = parse_users(xml_content)
        print(users)

        users_service.save_users(users)
        return (
            jsonify({"status": "success", "message": "Users uploaded successfully"}),
            200,
        )

    except Exception as e:
        traceback.print_exc()
        return (
            jsonify({"status": "error", "message": "Internal error", "detail": str(e)}),
            500,
        )


@admin_router.route("/users", methods=["GET"])
def get_all_users():
    """
    Retrieve all users from the service and return as JSON.
    """
    try:
        users = users_service.get_users()

        users_data = [
            {
                "id": user.user_id,
                "pwd": user.pwd,
                "NombreCompleto": user.full_name,
                "CorreoElectronico": user.email,
                "NumeroTelefono": user.phone_number,
                "Direccion": user.address,
                "perfil": user.profile_url,
            }
            for user in users
        ]

        return jsonify({"status": "success", "data": users_data}), 200

    except Exception as e:
        traceback.print_exc()
        return (
            jsonify({"status": "error", "message": "Internal error", "detail": str(e)}),
            500,
        )


@admin_router.route("/export/xml", methods=["GET"])
def export_users_as_xml():
    """
    Export all users to XML format and return as a response.
    """
    try:
        users = users_service.get_users()

        if not users:
            return jsonify({"status": "error", "message": "No users available"}), 404

        root = ET.Element("usuarios")
        for user in users:
            user_elem = ET.SubElement(
                root,
                "usuario",
                {"id": user.user_id, "pwd": user.pwd},
            )
            ET.SubElement(user_elem, "NombreCompleto").text = escape(user.full_name)
            ET.SubElement(user_elem, "CorreoElectronico").text = escape(user.email)
            ET.SubElement(user_elem, "NumeroTelefono").text = escape(user.phone_number)
            ET.SubElement(user_elem, "Direccion").text = escape(user.address)
            ET.SubElement(user_elem, "perfil").text = escape(user.profile_url)

            images_elem = ET.SubElement(user_elem, "imagenes")
            images = image_service.get_images_by_user_id(user.user_id)
            for image in images:
                image_elem = ET.SubElement(images_elem, "imagen", {"id": image.id})
                ET.SubElement(image_elem, "nombre").text = escape(image.name)

                design_elem = ET.SubElement(image_elem, "diseño")
                for pixel in image.pixels:
                    ET.SubElement(
                        design_elem,
                        "pixel",
                        {"fila": str(pixel.row), "col": str(pixel.column)},
                    ).text = escape(pixel.color)

        xml_str = minidom.parseString(
            ET.tostring(root, encoding="unicode")
        ).toprettyxml(indent="\t")

        return Response(xml_str, mimetype="application/xml", status=200)

    except Exception as e:
        traceback.print_exc()
        return (
            jsonify({"status": "error", "message": "Internal error", "detail": str(e)}),
            500,
        )
