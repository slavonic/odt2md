import lxml.etree as et
import lxmlx.event as ev
from odt2md.style import parse_styles, TextStyle, ParaStyle


content = '''\
<?xml version="1.0" encoding="UTF-8"?>
<office:document-content xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0"
    xmlns:loext="urn:org:documentfoundation:names:experimental:office:xmlns:loext:1.0" 
    xmlns:xlink="http://www.w3.org/1999/xlink"
    office:version="1.2">
    <office:automatic-styles>
        <style:style style:name="P1" style:family="paragraph" style:parent-style-name="Standard">
            <style:paragraph-properties fo:text-align="center" style:justify-single-word="false" fo:orphans="0" fo:widows="0"/>
            <style:text-properties fo:color="#ff0000" style:font-name="Ponomar Unicode" fo:font-size="17pt" fo:language="cu" fo:country="RU" style:text-underline-style="none" style:letter-kerning="true" style:font-size-asian="17pt" style:language-asian="none" style:country-asian="none" style:font-name-complex="Akathistos ieUcs" style:font-size-complex="20pt"/>
        </style:style>
        <style:style style:name="T1" style:family="text">
            <style:text-properties fo:color="#ff0000" fo:font-size="22pt" style:letter-kerning="true" style:font-size-asian="22pt" style:language-asian="none" style:country-asian="none" style:font-size-complex="28pt"/>
        </style:style>
        <style:style style:name="T2" style:family="text">
            <style:text-properties fo:color="#000000" fo:font-size="22pt" style:letter-kerning="true" style:font-size-asian="22pt" style:language-asian="none" style:country-asian="none" style:font-size-complex="28pt"/>
        </style:style>
    </office:automatic-styles>
    <office:body>
        <office:text text:use-soft-page-breaks="true">
            <text:p text:style-name="P1">
                <draw:frame draw:style-name="fr1" draw:name="Рисунок 107" text:anchor-type="as-char" svg:width="6.3299in" svg:height="1.1146in" draw:z-index="0">
                    <draw:image xlink:href="Pictures/100000000000036D00000093A10EF874767082E9.png" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad" loext:mime-type="image/png"/>
                </draw:frame>
            </text:p>
            <text:p text:style-name="P1">
                <text:span text:style-name="T1">Въ понедѣ́льникъ г҃</text:span>
                <text:span text:style-name="T2">-</text:span>
                <text:span text:style-name="T1">ѧ седми́цы на ᲂу҆́трени, </text:span>
            </text:p>
        </office:text>
    </office:body>
</office:document-content>
'''.encode()

xml = et.fromstring(content)

def test():
    styles = list(parse_styles(xml))
    assert styles == [
        ParaStyle(
            name='P1',
            text_align='center',
            font='Akathistos ieUcs',
            color='#ff0000',
            size='17pt',
            bold=None,
            italic=None,
        ),
        TextStyle(
            name='T1',
            font=None,
            color='#ff0000',
            size='22pt',
            bold=None,
            italic=None,
        ),
        TextStyle(
            name='T2',
            font=None,
            color='#000000',
            size='22pt',
            bold=None,
            italic=None,
        ),
    ]

