import re


def validate_email(email):
    """
    Validate email format using regex.
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_phone(phone):
    """
    Validate phone number (must be 8 digits).
    """
    return bool(re.match(r"^\d{8}$", phone))


def validate_user_id(user_id):
    """
    Validate user ID format (must start with 'IPC-' followed by numbers).
    """
    return bool(re.match(r"^IPC-\d+$", user_id))
