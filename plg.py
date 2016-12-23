#!/usr/bin/env python3
import argparse
import os
import requests

from PIL import Image, ImageDraw, ImageFont

PL_GALLERY_JSON_URL = "https://www.planet.com/gallery.json"


def get_json(url=PL_GALLERY_JSON_URL):
    """
    Get JSON from URL
    :param url: URL to fetch (defaults to Planet Gallery)
    :return: Parsed JSON
    """
    r = requests.get(url)
    # Fail fast, always should return 200, even if empty
    r.raise_for_status()
    return r.json()


def download_file(url, filepath):
    """
    Download the file
    :param url: URL of file to download
    :param filepath: Full path to save to
    :return: Success
    """

    r = requests.get(url)
    with open(filepath, 'wb') as file:
        file.write(r.content)


def draw_info(image_path, metadata, font_family='Arial.ttf', font_size=24, new_name=None):
    """
    Draw gallery info. WIP
    :param image_path: Path of image
    :param metadata: Dictionary of the gallery item
    :param font_family: Font family for text
    :param font_size: Font size for text
    :param new_name: New file name, otherwise overwrites original file
    :return:
    """

    # Open as RGBA so we can layer in the text
    image = Image.open(image_path).convert('RGBA')
    image_width, image_height = image.size

    # Drawing layer, since drawing directly on image doesn't seem to work
    text_image = Image.new('RGBA', image.size, (255, 255, 255, 0))

    # Text for the box
    text = "{} - {}\nImage © Planet".format(metadata['title'], metadata['acquisition_date'][:10])

    font = ImageFont.truetype(font_family, font_size)

    draw = ImageDraw.Draw(text_image)

    # Get text size so we know how big to draw the box
    text_width, text_height = draw.multiline_textsize(text, font)

    # For now, pad the box with half the height of the font
    box_padding = font_size / 2

    # Magic numbers for now of where it might look good
    box_x_margin = 30  # From left-side
    box_y_margin = 300  # From bottom

    # Box size is text size + padding on all sides
    box_width = text_width + (2 * box_padding)
    box_height = text_height + (2 * box_padding)

    # Start drawing at the right place, based on margin definitions
    x = box_x_margin
    y = image_height - box_height - box_y_margin

    # Draw rectangle
    draw.rectangle([(x, y), (x + box_width, y + box_height)], fill=(0, 0, 0, 100))

    # Draw text
    draw.multiline_text((x + box_padding, y + box_padding), text, fill=(255, 255, 255, 255), font=font)

    out = Image.alpha_composite(image, text_image)

    out.save(new_name if new_name else image_path)


def fetch_images(verbose=True, directory=".", overwrite=False, download_limit=10, newer=False, draw=False):
    gallery = get_json()
    downloads = 0

    for item in gallery:
        full_image_url = item['images']['full']

        filename = os.path.basename(full_image_url)  # Nice trick to get filename from URL
        filepath = os.path.join(directory, filename)
        if overwrite or not os.path.exists(filepath):
            if verbose:
                print("Downloading: {}".format(full_image_url))

            download_file(full_image_url, filepath)

            if verbose:
                print("Saved to: {}".format(filepath))

            if draw:
                draw_info(filepath, item)

                if verbose:
                    print("Drew info into image: {}".format(filepath))

            # Track number of downloads
            downloads += 1
            if downloads >= download_limit:
                break
        elif newer:
            if verbose:
                print("Stopping at image already existing: {}".format(filepath))
            break
        elif verbose:
            print("Skipping existing file: {}".format(filepath))


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'directory',
        type=str,
        default='.',
        help="Images output directory",
    )

    parser.add_argument(
        '-q', '--quiet',
        action='store_false',
        dest='verbose',
        default=True,
        help="Don't print anything",
    )

    parser.add_argument(
        '-o', '--overwrite',
        action='store_true',
        default=False,
        help="Get the image, even if it already exists. Ignores --newer flag.",
    )

    parser.add_argument(
        '-l', '--limit',
        type=int,
        default=10,
        help="Number of images to download [default: %(default)i]",
    )

    parser.add_argument(
        '-n', '--newer',
        action='store_true',
        default=False,
        help="Only get newer images. Script stops when it detects already-existing files.",
    )

    parser.add_argument(
        '-d', '--draw',
        action='store_true',
        dest='draw',
        default=False,
        help="Draw some basic info about the scene into the image",
    )

    args = parser.parse_args()

    directory = args.directory

    if not os.path.exists(directory):
        print("Directory doesn't exist: {}".format(directory))
        return 1

    fetch_images(
        verbose=args.verbose,
        directory=directory,
        overwrite=args.overwrite,
        download_limit=args.limit,
        newer=args.newer,
        draw=args.draw,
    )


if __name__ == "__main__":
    main()
