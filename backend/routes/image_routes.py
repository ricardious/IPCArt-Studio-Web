from flask import Blueprint, request, jsonify
from services.image_service import ImageService
from utils.xml_parser import parse_image
from xml.etree.ElementTree import ParseError

image_router = Blueprint("image", __name__)
image_service = ImageService()


@image_router.route("/add-image/<string:user_id>", methods=["POST"])
def add_image(user_id):
    """
    Adds an image for a given user.
    This function handles the process of receiving an XML file, parsing it, and adding the image to the system.
    It returns appropriate responses based on the success or failure of these operations.
    Args:
        user_id (int): The ID of the user to whom the image belongs.
    Returns:
        Response: A Flask JSON response with a status message and HTTP status code.
    Possible Responses:
        - 400: If no file is provided or the file content is empty.
        - 400: If there is an error parsing the XML content.
        - 201: If the image is added successfully, including the image ID and graph.
        - 409: If there is a conflict or error adding the image.
        - 500: If there is an internal server error.
    """
    try:
        if not request.data:
            return jsonify({"status": "error", "message": "No file provided."}), 400

        xml_content = request.data.decode("utf-8").strip()
        if not xml_content:
            return jsonify({"status": "error", "message": "Empty file content."}), 400

        try:
            image = parse_image(xml_content, user_id)
        except ParseError as e:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": f"XML Parsing Error: {e}",
                    }
                ),
                400,
            )

        image.id = None

        result = image_service.add_image(image)
        if result["success"]:
            return (
                jsonify(
                    {
                        "status": "success",
                        "message": "Image added successfully.",
                        "image_id": result["image_id"],
                        "graph": result["graph"],
                    }
                ),
                201,
            )
        else:
            return (jsonify({"status": "error", "message": result["message"]}), 409)

    except Exception as e:
        return (
            jsonify({"status": "error", "message": f"Internal Server Error: {e}"}),
            500,
        )


@image_router.route(
    "/transform-image/<string:image_id>/<string:filter_type>", methods=["POST"]
)
def transform_image(image_id, filter_type):
    """
    Transforms an image by applying a specified filter (grayscale or sepia).

    Args:
        image_id (str): The ID of the image to transform.
        filter_type (str): The type of filter to apply ('grayscale' or 'sepia').

    Returns:
        JSON response containing:
            - success (bool): Whether the transformation was successful.
            - image_id (str): The ID of the new transformed image.
            - graph (str): Base64-encoded graph of the transformed image.
            - message (str): Any relevant message or error details.
    """
    try:
        # Call the service to transform the image
        result = image_service.transform_image(image_id, filter_type)
        return (
            jsonify(
                {
                    "success": True,
                    "image_id": result["image_id"],
                    "original_graph": result["original_graph"],
                    "transformed_graph": result["transformed_graph"],
                    "message": "Image transformed successfully.",
                }
            ),
            200,
        )
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    except Exception as e:
        return (
            jsonify({"success": False, "message": f"Internal Server Error: {e}"}),
            500,
        )
