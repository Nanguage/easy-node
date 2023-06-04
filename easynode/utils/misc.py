
def hex_color_add_alpha(hex: str, alpha: int) -> str:
    """Add alpha to hex color.

    Args:
        hex (str): hex color, rgb or argb
        alpha (int): alpha value
            0 - 255
    """
    hex = hex.strip("#")
    if len(hex) == 8:
        # if already has alpha, change it
        hex = hex[2:]
    return f"#{alpha:02x}{hex}"
