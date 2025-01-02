class Pixel:
    """
    Represents a single pixel in a grid with its position and color.

    Attributes:
        row (int): The row index of the pixel in the grid.
        column (int): The column index of the pixel in the grid.
        color (str): The color of the pixel, represented as a string (e.g., "red", "#FF0000").
    """

    def __init__(self, row, column, color):
        """
        Initializes a Pixel instance with its row, column, and color.

        Args:
            row (int): The row index of the pixel.
            column (int): The column index of the pixel.
            color (str): The color of the pixel.
        """
        self.row = row  # Row position of the pixel
        self.column = column  # Column position of the pixel
        self.color = color  # Color of the pixel
