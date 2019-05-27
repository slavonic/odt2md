from dataclasses import dataclass
from odt2md.util import ns


@dataclass(frozen=True)
class TextStyle:
    name: str
    font: str=None
    color: str=None
    size: str=None
    bold: str=None
    italic: str=None

    @classmethod
    def effective_style(cls, styles):
        '''Given a list of styles, computes the effective style.
        Leftmost style in the list represents the top style in
        the hierarchy (least significant), while the rightmost one
        represents the bottom style (most significant).
        More significant srtyle overrides the values set by the less
        significant one.
        None value is interpreted as "inherit"
        '''
        fonts  = [s.font   for s in styles if s.font   is not None]
        colors = [s.color  for s in styles if s.color  is not None]
        sizes  = [s.size   for s in styles if s.size   is not None]
        bolds  = [s.bold   for s in styles if s.bold   is not None]
        italics= [s.italic for s in styles if s.italic is not None]

        font = fonts[-1] if fonts else None
        color = colors[-1] if colors else None
        size = sizes[-1] if sizes else None
        bold = bolds[-1] if bolds else None
        italic = italics[-1] if italics else None

        return cls(name=None, font=font, color=color, size=size, bold=bold, italic=italic)


@dataclass(frozen=True)
class ParaStyle(TextStyle):  # note that ParaStyle extends TextStyle
    text_align: str=None


def parse_styles(xml):
    for x in xml.findall('.//' + ns.style('style')):
        name = x.attrib.get(ns.style('name'))

        text_style = x.find('./'+ns.style('text-properties'))
        if text_style is not None:
            font_name = text_style.get(ns.style('font-name-complex'),
                text_style.get(ns.style('font-name')))
            font_size = text_style.get(ns.fo('font-size'))
            font_color = text_style.get(ns.fo('color'))
            font_bold = text_style.get(ns.fo('font-weight'))
            font_italic = text_style.get(ns.fo('font-style'))
            text_style = TextStyle(
                name=name,
                font=font_name,
                color=font_color,
                size=font_size,
                bold=font_bold,
                italic=font_italic
            )

        para_style = x.find('./'+ns.style('paragraph-properties'))
        if para_style is not None:
            text_align = para_style.get(ns.fo('text-align'))
            if text_style is not None:
                yield ParaStyle(
                    name=name,
                    text_align=text_align,
                    font=font_name,
                    color=font_color,
                    size=font_size,
                    bold=font_bold,
                    italic=font_italic
                )
            else:
                yield ParaStyle(
                    name=name,
                    text_align=text_align
                )
        elif text_style is not None:
            yield text_style
