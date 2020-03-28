import zipfile
import logging
import os
import lxml.etree as et
import lxmlx.event as ev
from odt2md.style import parse_styles
from odt2md.block import parse_odt
from odt2md.styler import Styler
from odt2md.util import ns


def odt2md(odt_name, zip_name, profile=None, max_line_width=128):
    with zipfile.ZipFile(odt_name) as z:
        with z.open('content.xml', 'r') as f:
            xml = et.fromstring(f.read())

        blocks = parse_odt(xml)
        styler = Styler(parse_styles(xml), profile_filename=profile, max_line_width=max_line_width)
        markdown_text = styler.format_md(blocks)

        with zipfile.ZipFile(zip_name, 'w') as zz:
            with zz.open('content.md', 'w') as f:
                f.write(markdown_text.encode())

            dedup = set()
            for image in styler.images:  # images were collected during styling
                if image in dedup:
                    continue
                dedup.add(image)
                with z.open(image, 'r') as f:
                    with zz.open(image, 'w') as ff:
                        ff.write(f.read())
                logging.info('written image: %s', image)

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Converts Libre Office ODT file to a ZIP file with CU-flavored Markdown')

    parser.add_argument('--verbose', '--v', action='count', default=0, help='Increase verbosity')
    parser.add_argument('--max_line_width', '-m', default=128, type=int, help='Cosmetic: break lines is longer than this value (default 128)')
    parser.add_argument('--profile', help='Filename of a custom profile')
    parser.add_argument('input', help='Input ODT file')
    parser.add_argument('output', help='Output ZIP file')

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    odt2md(args.input, args.output, profile=args.profile, max_line_width=args.max_line_width)


if __name__ == '__main__':
    main()
