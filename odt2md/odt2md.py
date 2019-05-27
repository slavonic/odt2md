import zipfile
import logging
import lxml.etree as et
import lxmlx.event as ev
from odt2md.style import parse_styles
from odt2md.block import parse_odt
from odt2md.profile import Profile
from odt2md.util import ns


def odt2md(odt_name, md_name):
    with zipfile.ZipFile(odt_name) as z:
        with z.open('content.xml', 'r') as f:
            xml = et.fromstring(f.read())

    blocks = parse_odt(xml)
    profile = Profile(parse_styles(xml))
    markdown_text = format_md(profile, blocks)

    with open(md_name, 'w') as f:
        f.write(markdown_text)


def format_md(profile, blocks):
    markdown_text = []
    for b in blocks:
        for text in profile.format_block(b):
            markdown_text.append(text)
    return ''.join(markdown_text)


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Converts Libre Office ODT file to CU-flavored Markdown')

    parser.add_argument('--verbose', '--v', action='count', default=0, help='Increase verbosity')
    parser.add_argument('input', help='Input ODT file')
    parser.add_argument('output', help='Input MD file')

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    odt2md(args.input, args.output)


if __name__ == '__main__':
    main()
