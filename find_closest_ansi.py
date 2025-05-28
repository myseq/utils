#!/usr/bin/env python3

import argparse

def hex_to_rgb(hex_str):
    """Converts a hex color code to an RGB tuple.

    Args:
        hex_str: The hex color code as a string, e.g., "a1e335".

    Returns:
        A tuple representing the RGB values (R, G, B).
    """
    hex_str = hex_str.strip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def find_closest_ansi_color(rgb_tuple, ansi_dict):
    """Finds the closest ANSI color to the given RGB tuple.

    Args:
        rgb_tuple: The target RGB tuple.
        ansi_dict: A dictionary mapping ANSI codes to RGB tuples.

    Returns:
        The closest ANSI code.
    """
    min_distance = float('inf')
    closest_code = None
    for ansi_code, ansi_rgb in ansi_dict.items():
        distance = sum((a - b)**2 for a, b in zip(rgb_tuple, ansi_rgb))
        if distance < min_distance:
            min_distance = distance
            closest_code = ansi_code
    return closest_code

def ansi_to_rgb(ansi_code):
    """Maps an ANSI 256-color code to its corresponding true RGB value.

    Args:
        ansi_code: The ANSI 256-color code.

    Returns:
        A tuple representing the RGB values (R, G, B).
    """

    if 0 <= ansi_code <= 15:
        # 16 basic colors
        colors = {
            0: (0, 0, 0),  # Black
            1: (0, 0, 170),  # Dark Blue
            2: (0, 170, 0),  # Dark Green
            3: (0, 170, 170),  # Dark Cyan
            4: (170, 0, 0),  # Dark Red
            5: (170, 0, 170),  # Dark Magenta
            6: (170, 85, 0),  # Dark Yellow
            7: (170, 170, 170),  # Gray
            8: (85, 85, 85),  # Dark Gray
            9: (85, 85, 255),  # Blue
            10: (85, 255, 85),  # Green
            11: (85, 255, 255),  # Cyan
            12: (255, 85, 85),  # Red
            13: (255, 85, 255),  # Magenta
            14: (255, 255, 85),  # Yellow
            15: (255, 255, 255),  # White
        }
        return colors.get(ansi_code)
    elif 16 <= ansi_code <= 231:
        # 216 colors
        r = (ansi_code - 16) // 36
        g = ((ansi_code - 16) % 36) // 6
        b = (ansi_code - 16) % 6
        return r * 40 + 55, g * 40 + 55, b * 40 + 55
    elif 232 <= ansi_code <= 255:
        # 24 grayscale colors
        gray = (ansi_code - 232) * 10 + 8
        return gray, gray, gray

def usage():
    """usage() function """
    parser = argparse.ArgumentParser(description='Find the closest ANSI color to a given hex color.')
    parser.add_argument('hex_color', type=str, help='The hex color code to match.')

    return parser.parse_args()


if __name__ == "__main__":
    """main() function """

    args = usage()

    ansi_dict = {}
    # Loop through all 256 ANSI colors and form a dict to hold the ANSI and RGB mapping
    for i in range(256):
        rgb_color = ansi_to_rgb(i)
        r, g,b = rgb_color
        ansi_dict[i] = rgb_color


    hex_color = args.hex_color
    rgb_color = hex_to_rgb(hex_color)

    closest_ansi_code = find_closest_ansi_color(rgb_color, ansi_dict)
    closest_ansi_rgb = ansi_to_rgb(closest_ansi_code)

    print(f'')
    r,g,b = rgb_color
    print(f'>>>> HEX code: \'#{hex_color}\' in \033[38;2;{r};{g};{b}mRGB\033[0m/{rgb_color}')
    r,g,b = closest_ansi_rgb
    print(f' [*] Closest : \033[38;5;{closest_ansi_code}mANSI code\033[0m/{closest_ansi_code:>3d} | \033[38;2;{r};{g};{b}mRGB\033[0m/({closest_ansi_rgb[0]:>3d},{closest_ansi_rgb[1]:>3d},{closest_ansi_rgb[2]:>3d})')
    print(f'')
    

