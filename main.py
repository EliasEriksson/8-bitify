from PIL import Image
from math import sqrt
from pathlib import Path
import time


def load_colour_palette(fp: str, width: int, height: int) -> list:
    # width and hight is the dimentions of each color in the palette
    img = Image.open(fp)
    colours = []
    for x in range(0, img.width, width):
        for y in range(0, img.height, height):
            colours.append(img.getpixel((x, y)))
    return colours


PALETTE = load_colour_palette("colour_palette_1px.png", 1, 1)


def bitify_color(img: Image, f_extention: str) -> None:
    exif = img.info["exif"] if "exif" in img.info else None
    t = time.perf_counter()
    for x in range(img.width):
        for y in range(img.height):
            distances = []
            r1, g1, b1, *_ = img.getpixel((x, y))
            for r2, g2, b2, *__ in PALETTE:
                distance = sqrt((r2-r1)**2 + (g2-g1)**2 + (b2-b1)**2)
                distances.append(distance)
            average = PALETTE[distances.index(min(distances))]
            img.putpixel((x, y), average)
        print(f"completed line {x} / {img.width}")
    print(time.perf_counter() - t)
    img.save(f"out{f_extention}", exif=exif)


if __name__ == '__main__':
    path = "me.png"
    extention = Path(path).suffix
    image = Image.open(path)
    bitify_color(image, extention)
