import lxml.etree as et
import lxmlx.event as ev
from odt2md.block import parse_blocks, ImageBlock, TextBlock, Span


content = '''\
<?xml version="1.0" encoding="UTF-8"?>
<office:text xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0"
    xmlns:loext="urn:org:documentfoundation:names:experimental:office:xmlns:loext:1.0" 
    xmlns:xlink="http://www.w3.org/1999/xlink"
    office:version="1.2">
            <text:p text:style-name="P1">
                <draw:frame draw:style-name="fr1" draw:name="Рисунок 107" text:anchor-type="as-char" svg:width="6.3299in" svg:height="1.1146in" draw:z-index="0">
                    <draw:image xlink:href="Pictures/100000000000036D00000093A10EF874767082E9.png" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad" loext:mime-type="image/png"/>
                </draw:frame>
            </text:p>
            <text:p text:style-name="P1"><text:span text:style-name="T1">Въ понедѣ́льникъ г҃</text:span><text:span text:style-name="T2">-</text:span><text:span text:style-name="T1">ѧ седми́цы на ᲂу҆́трени, </text:span></text:p>
</office:text>
'''.encode()

xml = et.fromstring(content)

def test():
    blocks = []
    for p in xml:
        blocks.extend(parse_blocks(p))
    assert blocks == [
        ImageBlock(name='Рисунок 107', href='Pictures/100000000000036D00000093A10EF874767082E9.png'),
        TextBlock(
            para_style='P1',
            spans=[
                Span(styles=['P1', 'T1'], text='Въ понедѣ́льникъ г҃'),
                Span(styles=['P1', 'T2'], text='-'),
                Span(styles=['P1', 'T1'], text='ѧ седми́цы на ᲂу҆́трени,'),
            ],
            footnotes=[]
        )
    ]

