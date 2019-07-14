import argparse
import json
import os.path
import requests
from subprocess import run
from subprocess import CalledProcessError

try:
    from mri_to_webp import parse_mri_data_to_webp_buffer
except ImportError:
    # yeap, I'm going full lazy here
    from mangarock.mri_to_webp import parse_mri_data_to_webp_buffer

from random import choice
from slugify import slugify
from time import sleep
from werkzeug.utils import secure_filename

query_version = 401


def make_series_info_uri(series_oid):
    # series_oid - mrs-serie-{series_num}
    return f"https://api.mangarockhd.com/query/web{query_version}/info?oid={series_oid}&last=0"


def make_chapter_data_uri(chapter_oid):
    return f"https://api.mangarockhd.com/query/web{query_version}/pages?oid={chapter_oid}"


def get_chapters(args, series_info):
    chapters = series_info['chapters']

    if args.chapters:
        of_interest = set(map(int, args.chapters.split(',')))
        chapters = filter(lambda c: c['order'] in of_interest, chapters)
        chapters = tuple(chapters)

    return chapters


def convert_to_png(filepath, png_filepath):
    try:
        run(["dwebp", "-quiet", filepath, "-o", png_filepath], check=True)

        print(f"{png_filepath} written to file")
        os.remove(filepath)  # we don't leave dirt behind
    except CalledProcessError:
        print("Could not create png image; do you have dwebp installed?")


def download_webp(mri_url, filepath):
    for i in range(3):
        mri_buffer = requests.get(mri_url).content

        if len(mri_buffer) > 0:
            break  # we got our data!

    # nothing to write
    if len(mri_buffer) == 0:
        return False

    webp_buffer = parse_mri_data_to_webp_buffer(mri_buffer)

    # writes the image
    with open(filepath, "wb") as fs:
        fs.write(bytes(webp_buffer))

    return True

def show_info_cmd(series_info):
    for key in sorted(series_info.keys()):
        value = series_info[key]

        if key in (
            'chapters', 'extra', 'characters',
            'categories', 'authors', 'artworks',
            'cover'
        ):
            continue

        print("%15s: " % key, end='')

        if key == 'rich_categories':
            print(', '.join(sorted(map(lambda v: v['name'], value))))
        elif key == 'direction':
            print(value == 1 and 'RL' or 'LR')
        elif type(value) == list:
            print(', '.join(value))
        else:
            print(value)


def main():
    argparser = create_argparser()
    args = argparser.parse_args()
    use_png = args.png  # no webp in this house, mister!
    show_info = args.show

    series_info_url = make_series_info_uri(args.series)
    series_info_json: dict = requests.get(series_info_url).json()
    series_info: dict = series_info_json['data']
    series_name = series_info['name']
    series_name_secure = secure_filename(series_name)
    series_dirpath = slugify(series_name_secure)
    series_info_filepath = os.path.join(series_dirpath, "info.json")

    if not os.path.exists(series_dirpath):
        os.mkdir(series_dirpath)

    if not os.path.exists(series_info_filepath):
        with open(series_info_filepath, "w") as fs:
            json.dump(series_info, fs)

    if show_info:
        show_info_cmd(series_info)
        exit(0)

    for chapter in get_chapters(args, series_info):
        chapter_name = chapter['name']
        chapter_name_secure = secure_filename(chapter_name)
        chapter_dirpath = os.path.join(series_dirpath, slugify(chapter_name_secure))
        chapter_cbz_filepath = f"{chapter_dirpath}.cbz"

        if os.path.exists(chapter_cbz_filepath):
            print(f"{chapter_cbz_filepath} found; chapter will not be downloaded")
            continue

        if not os.path.exists(chapter_dirpath):
            os.mkdir(chapter_dirpath)

        chapter_data_url = make_chapter_data_uri(chapter['oid'])
        chapter_data = requests.get(chapter_data_url).json()

        # at least one image download failed?
        has_failed_download = False

        for index, mri_url in enumerate(chapter_data['data']):
            filename = f"{index:03}.webp"
            filepath = os.path.join(chapter_dirpath, filename)

            webp_exists = os.path.exists(filepath) and (os.path.getsize(filepath) > 0)

            png_filename = f"{index:03}.png"
            png_filepath = os.path.join(chapter_dirpath, png_filename)

            png_exists =\
                use_png and\
                os.path.exists(png_filepath) and\
                (os.path.getsize(png_filepath) > 0)

            if use_png and png_exists:
                print(f"skipping {png_filename}")
                continue

            if not use_png and webp_exists:
                print(f"skipping {filename}")
                continue

            download_ok = True

            if not webp_exists:
                if download_webp(mri_url, filepath):
                    print(f"{filepath} written to file")
                else:
                    download_ok = False
                    has_failed_download = True

            if use_png and download_ok:
                convert_to_png(filepath, png_filepath)

            sleep(choice([0.1, 0.2, 0.3, 0.4, 0.5]))

        print(f"{chapter_name_secure} downloaded" + (has_failed_download and ' [fail]' or ''))


def create_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('series', help='series oid')
    parser.add_argument('-c', '--chapters', nargs='?', help='comma separated chapter index list')
    parser.add_argument('-p', '--png', action="store_true", help='save images as png')
    parser.add_argument('-s', '--show', action='store_true', help='show manga info')
    return parser


if __name__ == '__main__':
    main()
