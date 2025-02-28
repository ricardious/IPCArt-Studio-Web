from flask import Blueprint, request, jsonify
from services.image_service import ImageService
from utils.xml_parser import parse_image
from xml.etree.ElementTree import ParseError

statistics_router = Blueprint("statistics", __name__)
image_service = ImageService()


@statistics_router.route("/top-users", methods=["GET"])
def get_top_users():
    try:
        # Obtener todas las imágenes
        gallery_images = image_service.get_all_gallery_images()

        # Contar las imágenes por usuario
        user_counts = {}
        for image in gallery_images:
            user_id = image["id_usuario"]
            user_counts[user_id] = user_counts.get(user_id, 0) + 1

        # Ordenar y obtener los top 3
        sorted_users = sorted(user_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        top_users = [
            {"user_id": user_id, "image_count": count}
            for user_id, count in sorted_users
        ]

        return jsonify({"status": "success", "data": top_users})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@statistics_router.route("/edited-images", methods=["GET"])
def get_edited_images():
    try:
        # Obtener todas las imágenes
        gallery_images = image_service.get_all_gallery_images()

        # Filtrar imágenes editadas y contarlas por usuario
        edited_counts = {}
        for image in gallery_images:
            if image.get("editado") == "1":  # Verifica que sean imágenes editadas
                user_id = image["id_usuario"]
                edited_counts[user_id] = edited_counts.get(user_id, 0) + 1

        # Ordenar en orden descendente
        sorted_edited_users = sorted(
            edited_counts.items(), key=lambda x: x[1], reverse=True
        )
        edited_users = [
            {"user_id": user_id, "edited_count": count}
            for user_id, count in sorted_edited_users
        ]

        return jsonify({"status": "success", "data": edited_users})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
