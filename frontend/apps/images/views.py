import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings


GLOBAL_CONTEXT = {"file_content": None, "image_preview": None}
ENDPOINT = settings.BACKEND_ENDPOINT


def gallery(request):
    user = request.session.get("user")
    if not user:
        messages.error(request, "Please log in to access this page.")
        return redirect("/login")

    context = {"user": user, "images": []}

    try:
        flask_url = f"{ENDPOINT}image/gallery"
        response = requests.get(flask_url)

        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                context["images"] = data.get("gallery", [])
            else:
                messages.error(
                    request, data.get("message", "Unknown error retrieving gallery.")
                )
        else:
            messages.error(request, "Failed to retrieve gallery from server.")
    except requests.RequestException as e:
        messages.error(request, f"Connection error: {str(e)}")
    except Exception as e:
        messages.error(request, f"Unexpected error: {str(e)}")

    return render(request, "images/gallery.html", context)


def upload(request):
    user = request.session.get("user")
    if not user:
        messages.error(request, "Please log in to access this page.")
        return redirect("/login")

    context = {
        "user": user,
        "xml_content": GLOBAL_CONTEXT.get("file_content"),
        "image": "",
    }

    if request.method == "POST":
        if "preview_file" in request.POST:
            if "file" in request.FILES:
                uploaded_file = request.FILES["file"]
                try:
                    file_content = uploaded_file.read().decode("utf-8")
                    context["xml_content"] = file_content
                    GLOBAL_CONTEXT["file_content"] = file_content
                except Exception as e:
                    messages.error(request, f"Error reading XML file: {str(e)}")
            else:
                messages.error(request, "Please select an XML file")

        elif "process_xml" in request.POST:
            xml_content = request.POST.get("xml_content")
            if xml_content:
                try:
                    flask_url = f"{ENDPOINT}image/add-image/{user['username']}"
                    headers = {"Content-Type": "application/xml"}

                    response = requests.post(
                        flask_url,
                        data=xml_content.encode("utf-8"),
                        headers=headers,
                    )

                    if response.status_code == 201:
                        data = response.json()
                        graph_base64 = data.get("graph")
                        context["image"] = graph_base64

                        messages.success(
                            request, "Image successfully processed and generated"
                        )
                    else:
                        messages.error(
                            request,
                            f"Error processing image: {response.json().get('message', 'Unknown error')}",
                        )
                except requests.RequestException as e:
                    messages.error(request, f"Server connection error: {str(e)}")
                except Exception as e:
                    messages.error(request, f"Unexpected error: {str(e)}")
            else:
                messages.error(request, "No XML content to process")

    return render(request, "images/upload_image.html", context)


def image_editor(request):
    user = request.session.get("user")
    if not user:
        messages.error(request, "Please log in to access this page.")
        return redirect("/login")

    context = {
        "user": user,
        "original_image": None,
        "processed_image": None,
    }

    if request.method == "POST":
        image_id = request.POST.get("image_id")
        filter_type = request.POST.get("filter_type")

        if not image_id:
            messages.error(request, "Please enter an image ID.")
            return render(request, "images/image_editor.html", context)

        if filter_type not in ["grayscale", "sepia", "negative"]:
            messages.error(
                request, "Invalid filter type. Use 'grayscale','sepia', or 'negative'."
            )
            return render(request, "images/image_editor.html", context)

        try:
            # Send request to Flask backend
            flask_url = f"{ENDPOINT}image/transform-image/{image_id}/{filter_type}"
            response = requests.post(flask_url)

            if response.status_code == 200:
                data = response.json()
                context["processed_image"] = (
                    f"data:image/svg+xml;base64,{data['transformed_graph']}"
                )
                context["original_image"] = (
                    f"data:image/svg+xml;base64,{data.get('original_graph', '')}"
                )
                messages.success(request, "Image successfully transformed.")
            else:
                messages.error(
                    request,
                    f"Error transforming image: {response.json().get('message', 'Unknown error')}",
                )
        except requests.RequestException as e:
            messages.error(request, f"Connection error: {str(e)}")
        except Exception as e:
            messages.error(request, f"Unexpected error: {str(e)}")

    return render(request, "images/image_editor.html", context)


def help_view(request):
    user = request.session.get("user")
    if not user:
        messages.error(request, "Please log in to access this page.")
        return redirect("/login")

    return render(request, "images/help.html", {"user": user})
