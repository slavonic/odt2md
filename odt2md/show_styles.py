'''
Shows styles in ODT (LibreOffice) file

Useful for creating conversion profiles
'''
import zipfile
import re
import collections
import lxml.etree as et
import lxmlx.event as ev
from odt2md.style import parse_styles, ParaStyle
from odt2md.block import TextBlock, parse_odt
from odt2md.util import ns


def show_styles(odt_name):
    with zipfile.ZipFile(odt_name) as z:
        with z.open('content.xml', 'r') as f:
            xml = et.fromstring(f.read())

    seen_styles = set()
    for b in parse_odt(xml):
        if type(b) is TextBlock:
            for span in b.spans:
                seen_styles.update(span.styles)

    def format(style_name, text_align, font, size, color, bold, italic):
        print(f'{style_name:<10} {text_align:<10} {font:<25} {size:<15} {color:<15} {bold:<10} {italic:<15}')

    format('Name', 'Text Align', 'Font', 'Size', 'Color', 'Bold', 'Italic')
    format('----', '----------', '----', '----', '-----', '----', '------')
    for s in parse_styles(xml):
        if s.name in seen_styles:
            format(
                s.name,
                '' if type(s) is not ParaStyle else s.text_align or '',
                s.font or '',
                s.size or '',
                s.color or '',
                s.bold or '',
                s.italic or '',
            )


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Lists active styles of a LibreOffice document')
    parser.add_argument('input', help='Input LibreOffice document')

    args = parser.parse_args()

    show_styles(args.input)


if __name__ == '__main__':
    main()

