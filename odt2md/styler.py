import itertools
import logging
from odt2md.block import Span, FootnoteRef, ImageBlock, TextBlock
from odt2md.style import ParaStyle, TextStyle
from odt2md.util import escape as E
from odt2md.emphasis import MarkdownStyle
from odt2md.util import split_into_lines
from odt2md import res


def read_profile(profile_filename):
    '''
    Reads profile file from disk.

    Profile is a normal Python source file, that must define a function named
    `profile`. Function must take the following parameters:

    * `font`
    * `color`
    * `size`
    * `bold`
    * `italic`

    and return an instance of `odt2md.emphasis.MarkdownStyle`.
    '''
    g = {}
    with open(profile_filename) as f:
        exec(f.read(), g)
    if 'profile' not in g:
        raise ValueError(f'profile {profile_filename} is expected to define a function named "profile"')
    if not callable(g['profile']):
        raise ValueError(f'name "profile" in {profile_filename} must be a function')

    return g['profile']

class Styler:
    def __init__(self, styles, profile_filename=None, max_line_width=128):
        self._style_index = {
            s.name: s for s in styles
        }

        if profile_filename is None:
            profile_filename = res('profile.py')

        self.profile_map = read_profile(profile_filename)

        self.images = []
        self.max_line_width = max_line_width

    def format_block(self, b):
        if type(b) is ImageBlock:
            yield f'![{E(b.name)}]({E(b.href)})\n\n'
            self.images.append(b.href)
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
                yield normalize_text(markdown_text, max_line_width=self.max_line_width) + '\n'

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

    def format_md(self, blocks):
        markdown_text = []
        for b in blocks:
            for text in self.format_block(b):
                markdown_text.append(text)
        return ''.join(markdown_text)



def normalize_text(text, max_line_width=128):
    return '\n'.join(split_into_lines(text, max_line_width=max_line_width))


