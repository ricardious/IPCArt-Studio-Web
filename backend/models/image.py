class Image:
    """
    Represents an image with its attributes.

    Attributes:
        id (str): Unique identifier for the image.
        user_id (str): ID of the user associated with the image.
        name (str): Name of the image.
        pixels (list): Pixel data of the image.
        edited (bool): Indicates if the image has been edited (default is False).
    """

    def __init__(self, id, user_id, name, pixels):
        """
        Initializes an Image instance.

        Args:
            id (str): Unique identifier for the image.
            user_id (str): ID of the user associated with the image.
            name (str): Name of the image.
            pixels (list): Pixel data of the image.
        """
        self.id = id
        self.user_id = user_id
        self.name = name
        self.pixels = pixels
        self.edited = False  # Default value for edited status
