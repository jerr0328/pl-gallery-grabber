#!/usr/bin/env python3
import argparse
import os
import requests

PL_GALLERY_JSON_URL = os.getenv("PL_GALLERY_JSON_URL", "https://www.planet.com/gallery.json")


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


def fetch_images(verbose=True, directory=".", overwrite=False, limit=10, skip_existing=False):
    gallery = get_json()
    counter = 0

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

            # Track downloads
            counter += 1

        else:
            if verbose:
                print("Skipping existing file: {}".format(filepath))
            # Increment counter unless otherwise specified
            if not skip_existing:
                counter += 1

        # Stop if the limit has been reached
        if counter >= limit:
            break


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
        help="Number of items to check [default: %(default)i]",
    )

    parser.add_argument(
        '-s', '--skip-existing',
        action='store_true',
        dest='skip_existing',
        default=False,
        help="Don't count existing files towards the limit.",
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
        limit=args.limit,
        skip_existing=args.skip_existing)


if __name__ == "__main__":
    main()
