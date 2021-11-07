import numpy as np

def create_color_list(levels: int) -> list:
    """
        Creates a list of colors that are in the garadient between start_color and end_color.
        It returns 'levels' numbers of colors
    """
    start_color = np.array([47, 47, 255])
    end_color = np.array([247, 0, 0])
    
    vector = end_color - start_color

    color_pallete = []

    for n in range(0, levels):
        color = start_color + (n / (levels - 1) * vector).astype(int)
        color_pallete.append('#%02x%02x%02x' % (color[0], color[1], color[2]))

    return color_pallete
