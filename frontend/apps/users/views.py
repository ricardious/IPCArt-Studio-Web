import requests
from django.shortcuts import render, redirect
from django.contrib import messages


def login_view(request):
    if request.method == "POST":
        # Capturar los datos enviados por el formulario
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            messages.error(request, "Username and password are required.")
            return redirect("/login")

        # URL del backend Flask
        flask_login_url = "http://127.0.0.1:4000/auth/login"

        try:
            # Enviar solicitud al backend Flask
            response = requests.post(
                flask_login_url, json={"username": username, "password": password}
            )
            if response.status_code == 200:
                data = response.json()
                messages.success(request, data.get("message", "Login successful!"))
                # Redirigir según el rol del usuario
                if data.get("role") == "admin":
                    return redirect("/admin/dashboard")  # Redirigir al panel de admin
                else:
                    return redirect("/user/home")  # Redirigir al inicio de usuario
        except requests.exceptions.RequestException as e:
            # Manejar errores de conexión
            messages.error(
                request, f"Error connecting to the authentication server: {str(e)}"
            )
    return render(request, "login.html")
