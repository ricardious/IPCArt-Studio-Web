import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import plotly.graph_objs as go
from plotly.offline import plot


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
                print(file_content)
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
    # Definir las URLs de los endpoints en Flask
    top_users_url = f"{ENDPOINT}statistics/top-users"
    edited_images_url = f"{ENDPOINT}statistics/edited-images"

    try:
        # Realizar solicitudes GET a los endpoints de Flask
        top_users_response = requests.get(top_users_url)
        edited_images_response = requests.get(edited_images_url)

        # Verificar el estado de las respuestas
        if (
            top_users_response.status_code == 200
            and edited_images_response.status_code == 200
        ):
            top_users_data = top_users_response.json().get("data", [])
            edited_images_data = edited_images_response.json().get("data", [])

            # Preparar datos para los gráficos
            # Gráfico 1: Top 3 usuarios con más imágenes cargadas
            usernames_top = [user["user_id"] for user in top_users_data]
            images_uploaded = [user["image_count"] for user in top_users_data]

            bar1 = go.Bar(
                x=usernames_top,
                y=images_uploaded,
                name="Top 3 Users with Most Uploaded Images",
            )

            # Gráfico 2: Cantidad de imágenes editadas por usuario en orden descendente
            usernames_edit = [user["user_id"] for user in edited_images_data]
            images_edited_count = [user["edited_count"] for user in edited_images_data]

            bar2 = go.Bar(
                x=usernames_edit,
                y=images_edited_count,
                name="Images Edited by Each User",
                marker=dict(color="mediumpurple"),
            )

            # Configurar los gráficos
            layout1 = go.Layout(
                plot_bgcolor="rgba(0,0,0,0)",  # Fondo del gráfico transparente
                paper_bgcolor="rgba(0,0,0,0)",  # Fondo del contenedor transparente
                font=dict(color="white"),  # Texto en blanco para modo oscuro
                autosize=True,
            )
            layout2 = go.Layout(
                plot_bgcolor="rgba(0,0,0,0)",  # Fondo del gráfico transparente
                paper_bgcolor="rgba(0,0,0,0)",  # Fondo del contenedor transparente
                font=dict(color="white"),  # Texto en blanco para modo oscuro
                autosize=True,
            )

            # Crear figuras de los gráficos
            fig1 = go.Figure(data=[bar1], layout=layout1)
            fig2 = go.Figure(data=[bar2], layout=layout2)

            # Convertir gráficos a div
            plot_div1 = plot(fig1, include_plotlyjs=False, output_type="div")
            plot_div2 = plot(fig2, include_plotlyjs=False, output_type="div")

            # Incluir estilo inline para ajustarlo al contenedor
            plot_div1 = f'<div style="width: 100%; height: 100%;">{plot_div1}</div>'
            plot_div2 = f'<div style="width: 100%; height: 100%;">{plot_div2}</div>'

            # Pasar los gráficos al contexto
            context = {
                "plot_div1": plot_div1,
                "plot_div2": plot_div2,
            }

            return render(request, "users/statistics.html", context)
        else:
            # Manejar errores si las respuestas no son exitosas
            messages.error(request, "Failed to fetch statistics from Flask backend.")
            return render(request, "users/statistics.html", {})
    except requests.exceptions.RequestException as e:
        # Manejar errores de conexión
        messages.error(request, f"Error connecting to Flask backend: {e}")
        return render(request, "users/statistics.html", {})


def logout(request):
    # Clear the session
    request.session.flush()
    return redirect("/login")
