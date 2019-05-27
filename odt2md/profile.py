import itertools
import logging
from odt2md.block import Span, FootnoteRef, ImageBlock, TextBlock
from odt2md.style import ParaStyle, TextStyle
from odt2md.util import escape as E
from odt2md.emphasis import MarkdownStyle
from odt2md.util import split_into_lines


def default_profile_map(font, color, size, bold, italic):
    '''
    Default transformation from LibreOffice to Markdown style
    '''
    bold = (bold == 'bold')
    italic = (italic == 'italic')
    kinovar = (color == '#ff0000')

    return MarkdownStyle(
        bold=bold,
        italic=italic,
        kinovar=kinovar,
        wide=False
    )


class Profile:
    def __init__(self, styles, profile_map=default_profile_map):
        self._style_index = {
            s.name: s for s in styles
        }
        self.profile_map = profile_map

    def format_block(self, b):
        if type(b) is ImageBlock:
            yield f'![{E(b.name)}]({E(b.href)})\n\n'
        else:
            assert type(b) is TextBlock
            if b.spans:
                # transform inline styles to markdown
                # and escape markdown text
                spans = []
                for span in b.spans:
                    if type(span) is Span:
                        spans.append( (span.styles, E(span.text)) )
                    elif type(span) is FootnoteRef:
                        spans.append( (span.styles, f'[^{E(span.citation)}]') )
                    else:
                        assert False, span

                markdown_text = ''.join(self.format_spans(spans))
                yield normalize_text(markdown_text) + '\n'

                if b.para_style is not None:
                    para_style = self._as_style(b.para_style)
                    if type(para_style) is ParaStyle and para_style.text_align == 'center':
                        yield '{{text_align=center}}\n'

                yield '\n'  # empty line separates markdown blocks

            for fnote in b.footnotes:
                yield f'[^{E(fnote.citation)}]: '
                is_first = True
                for bb in fnote.body:
                    if not is_first:
                        yield '    '   # indent footnote blocks, except the first one
                    yield from self.format_block(bb)
                    is_first = False

    def _as_style(self, name):
        x = self._style_index.get(name)
        if x is None:
            logging.warning('Undefined style name: %r', name)
            x = TextStyle(name)
            self._style_index[name] = x
        return x

    def format_spans(self, spans):

        markdown_spans = []

        for styles, text in spans:
            ss = [self._as_style(x) for x in styles]
            ss = [x for x in ss if x is not None]  # filter out unresolved styles
            effective_style = TextStyle.effective_style(ss)

            markdown_style = self._as_markdown_style(effective_style)

            markdown_spans.append( (markdown_style, text) )

        # merge together aliased markdown styles
        markdown_spans = itertools.groupby(markdown_spans, lambda x: x[0])
        markdown_spans = [
            (k, ''.join(y[1] for y in g))
            for k,g in markdown_spans
        ]

        for s,t in markdown_spans:
            leading_space = ' ' if t.startswith(' ') else ''
            trailing_space = ' ' if t.endswith(' ') else ''
            t = t.strip()

            if leading_space:
                yield leading_space
            yield from s(t)
            if trailing_space:
                yield trailing_space

    def _as_markdown_style(self, text_style):
        return self.profile_map(
            text_style.font,
            text_style.color,
            text_style.size,
            text_style.bold,
            text_style.italic
        )


def normalize_text(text):
    return '\n'.join(split_into_lines(text))


