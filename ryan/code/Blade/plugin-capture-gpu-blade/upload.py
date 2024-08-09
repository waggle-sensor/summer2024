import sys
import argparse
from waggle.plugin import Plugin


def run(args):
    print(f'uploading {args.file_path}')
    with Plugin() as plugin:
        plugin.upload_file(args.file_path)
        print(f'Done')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--file-path', dest='file_path',
        action='store', required=True, type=str,
        help='Path to file to upload')
    args = parser.parse_args()
    exit(run(args))