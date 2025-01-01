import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse

GLOBAL_CONTEXT = {"file_content": None, "binary_file": None, "file_name": None}
ENDPOINT = "http://localhost:4000/"


from django.shortcuts import render, redirect
from django.contrib import messages
import requests

GLOBAL_CONTEXT = {"file_content": None, "binary_file": None, "file_name": None}
ENDPOINT = "http://localhost:4000/"


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            messages.error(request, "Username and password are required.")
            return redirect("/login")

        flask_login_url = f"{ENDPOINT}auth/login"
        try:
            # Iniciar sesión en Flask
            response = requests.post(
                flask_login_url, json={"username": username, "password": password}
            )
            if response.status_code == 200:
                data = response.json()
                user_role = data.get("role")  # Obtener el rol del usuario
                if user_role == "admin":
                    # Guardar solo los datos relevantes para admin
                    request.session["user"] = {
                        "username": username,
                        "role": "admin",
                    }
                    messages.success(request, "Welcome, Admin!")
                    return redirect("/admin/dashboard")
                else:
                    # Obtener los datos adicionales del usuario regular
                    user_id = data.get("user_id")
                    user_response = requests.get(f"{ENDPOINT}user/{user_id}")
                    if user_response.status_code == 200:
                        user_data = user_response.json()["data"]
                        # Guardar los datos del usuario regular en la sesión
                        request.session["user"] = {
                            "username": username,
                            "role": user_role,
                            "full_name": user_data["full_name"],
                            "email": user_data["email"],
                            "profile_url": user_data["profile_url"],
                        }
                        messages.success(request, "Login successful!")
                        return redirect("/user/gallery")
                    else:
                        messages.error(request, "Failed to fetch user details.")
            else:
                messages.error(request, data.get("message", "Invalid credentials."))
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Error connecting to the server: {str(e)}")

    return render(request, "users/login.html")


def admin_dashboard(request):
    return render(request, "users/admin_dashboard.html")


def bulk_upload(request):
    context = {
        "file_uploaded": False,
        "uploaded_files": [],
        "file_content": GLOBAL_CONTEXT["file_content"],
        "file_name": GLOBAL_CONTEXT["file_name"],
    }

    flask_upload_url = f"{ENDPOINT}admin/bulk-upload"

    if request.method == "POST":
        uploaded_files = request.FILES.getlist("file")

        if not uploaded_files:
            messages.error(request, "No files uploaded.")
            return render(request, "users/bulk_upload.html", context)

        errors = []
        for file in uploaded_files:
            try:
                file_content = file.read()

                try:
                    decoded_content = file_content.decode("utf-8")
                    GLOBAL_CONTEXT["file_content"] = decoded_content
                    GLOBAL_CONTEXT["binary_file"] = file_content
                    GLOBAL_CONTEXT["file_name"] = file.name
                    context["file_content"] = decoded_content
                    context["file_name"] = file.name
                except UnicodeDecodeError:
                    messages.warning(request, f"{file.name} is not a valid text file.")

                file.seek(0)
                response = requests.post(
                    flask_upload_url,
                    files={"file": (file.name, file_content, file.content_type)},
                )

                if response.status_code == 200:
                    context["uploaded_files"].append(
                        {
                            "name": file.name,
                            "size": f"{file.size / 1024:.2f} KB",
                            "progress_percentage": 100,
                        }
                    )
                    context["file_uploaded"] = True
                else:
                    errors.append(f"Error processing {file.name}: {response.text}")

            except requests.exceptions.RequestException as e:
                errors.append(f"Could not connect to Flask for {file.name}: {str(e)}")
            except Exception as e:
                errors.append(f"Error processing {file.name}: {str(e)}")

        if errors:
            messages.error(request, " ".join(errors))
        else:
            messages.success(request, "Files uploaded successfully.")

    if request.GET.get("show_content"):
        context["file_content"] = GLOBAL_CONTEXT["file_content"]

    return render(request, "users/bulk_upload.html", context)


def view_users(request):
    # URL del endpoint de Flask
    flask_upload_url = f"{ENDPOINT}admin/users"

    try:
        response = requests.get(flask_upload_url)
        response_data = response.json()

        if response_data["status"] == "success":
            users = response_data["data"]
        else:
            users = []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching users: {e}")
        users = []

    return render(request, "users/view_users.html", {"users": users})


def view_xml(request):
    flask_export_url = f"{ENDPOINT}admin/export/xml"
    context = {"xml_content": None}

    try:
        # Solicitud GET al endpoint para obtener el contenido XML
        response = requests.get(flask_export_url)

        if response.status_code == 200:
            # Asignar el contenido XML al contexto
            context["xml_content"] = response.text
        else:
            # Manejar errores del servidor Flask
            messages.error(request, f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        # Manejar errores de conexión
        messages.error(request, f"Error connecting to the server: {str(e)}")

    return render(request, "users/view_xml.html", context)


def statistics(request):
    return render(request, "users/statistics.html")


def logout(request):
    # Clear the session
    request.session.flush()
    return redirect("/login")
