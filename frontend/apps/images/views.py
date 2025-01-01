from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages


def gallery(request):
    # Verificar si el usuario está autenticado
    if not request.session.get("full_name"):
        messages.error(request, "Please log in to access this page.")
        return redirect("/login")

    # Extraer datos del usuario desde la sesión
    user_data = {
        "full_name": request.session.get("full_name"),
        "email": request.session.get("email"),
        "profile_url": request.session.get("profile_url"),
        "role": request.session.get("role"),  # Pasar el rol al contexto
    }

    return render(request, "images/gallery.html", {"user": user_data})
