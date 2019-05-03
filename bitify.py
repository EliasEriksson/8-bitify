from PIL import Image
from pathlib import Path
import argparse


def swap_palette(img: Image, colors: int) -> Image:
    return img.convert("P", colors=colors, palette=Image.ADAPTIVE).convert("RGB")


def resize(img: Image, width: int, height: int) -> Image:
    return img.resize((width, height), resample=Image.NEAREST)


def bitify(path: str, color_bit: int = None,
           resolution: int = None, new_name: str = None) -> None:
    extention = Path(path).suffix
    img = Image.open(path)
    exif = img.info["exif"] if "exif" in img.info else None
    og_width, og_height = img.size

    if resolution:
        aspect_ratio = og_height / og_width
        height = int(aspect_ratio * resolution)
        img = resize(img, resolution, height)
        img = resize(img, og_width, og_height)
    if color_bit:
        img = swap_palette(img, 2**color_bit)

    if new_name:
        if extention:
            img.save(Path(new_name).absolute(), exif=exif)
        else:
            img.save(Path(f"{new_name}.png").absolute(), exif=exif)
    else:
        if extention:
            img.save(Path(f"{Path(path).stem}_modified{extention}"), exif=exif)
        else:
            img.save(Path(f"{Path(path).stem}_modified{Path(path).suffix}"), exif=exif)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='"8-bitify" an image.')
    parser.add_argument("file", type=str,
                        help="The file to process.")
    parser.add_argument("-c", "--color_bit", type=int,
                        help="The size of the color palette.")
    parser.add_argument("-r", "--resolution", type=int,
                        help="The downscaled resolution example 1080.")
    parser.add_argument("-n", "--new_name", type=str,
                        help="The new file name.")
    args = parser.parse_args()

    bitify(args.file, color_bit=args.color_bit,
           resolution=args.resolution, new_name=args.new_name)

