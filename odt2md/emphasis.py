from dataclasses import dataclass
from odt2md.util import is_single_letter


@dataclass(frozen=True)
class MarkdownStyle:
    bold:    bool = False # **xxxx**
    italic:  bool = False # *xxxx*
    kinovar: bool = False # =xxxx=
    wide:    bool = False # +xxxx+

    def __call__(self, text):
        if not text:
            return

        if self.bold:
            yield '**'
        if self.italic:
            yield '*'
        if self.wide:
            yield '+'

        if self.kinovar:
            words = text.split()
            assert words
            if is_single_letter(words[-1]):
                if len(words) > 1:
                    yield '=' + ' '.join(words[:-1]) + '= '
                yield '~' + words[-1]
            else:
                yield '=' + text + '='
        else:
            yield text

        if self.wide:
            yield '+'
        if self.italic:
            yield '*'
        if self.bold:
            yield '**'
