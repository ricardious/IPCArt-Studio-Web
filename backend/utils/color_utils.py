def hex_to_rgb(hex_color):
    """
    Converts a HEX color (#RRGGBB) to RGB (R, G, B).

    Args:
        hex_color (str): Color in HEX format (#RRGGBB).

    Returns:
        tuple: A tuple (R, G, B) with the RGB values.

    Raises:
        ValueError: If the HEX color is not exactly 7 characters (including '#')
                    or if it contains invalid characters.
    """
    if hex_color.startswith("#"):
        hex_color = hex_color[1:]
    if len(hex_color) != 6:
        raise ValueError("The HEX color must be exactly 6 characters after '#'.")
    try:
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
    except ValueError:
        raise ValueError("The HEX color contains invalid characters.")
    return r, g, b


def rgb_to_hex(r, g, b):
    """
    Converts an RGB (R, G, B) color to HEX (#RRGGBB).

    Args:
        r (int): Red component (0-255).
        g (int): Green component (0-255).
        b (int): Blue component (0-255).

    Returns:
        str: Color in HEX format (#RRGGBB).

    Raises:
        ValueError: If any of the RGB values are not in the range 0-255.
    """
    if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
        raise ValueError("RGB values must be between 0 and 255.")
    return f"#{r:02x}{g:02x}{b:02x}"


# Usage example (commented to prevent unintended execution):
# if __name__ == "__main__":
#     try:
#         hex_color = "#4CAF50"
#         rgb = hex_to_rgb(hex_color)
#         print(f"HEX {hex_color} to RGB: {rgb}")
#
#         new_hex = rgb_to_hex(*rgb)
#         print(f"RGB {rgb} to HEX: {new_hex}")
#     except ValueError as e:
#         print(f"Error: {e}")
