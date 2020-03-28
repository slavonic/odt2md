import regex
from enum import Enum

# XML Namespaces
class ns(Enum):
    office = lambda x: f'{{urn:oasis:names:tc:opendocument:xmlns:office:1.0}}{x}'
    text   = lambda x: f'{{urn:oasis:names:tc:opendocument:xmlns:text:1.0}}{x}'
    style  = lambda x: f'{{urn:oasis:names:tc:opendocument:xmlns:style:1.0}}{x}'
    drawing= lambda x: f'{{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}}{x}'
    xlink  = lambda x: f'{{http://www.w3.org/1999/xlink}}{x}'
    fo     = lambda x: f'{{urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0}}{x}'


def split_into_lines(text, max_line_width=128):
    text = regex.sub(r'\s+', ' ', text).strip().split()

    out = []
    out_len = 0
    for token in text:
        if out:
            if out_len + 1 + len(token) > max_line_width:
                yield ' '.join(out)
                out.clear()
                out_len = 0
            else:
                out.append(token)
                out_len += 1 + len(token)
        if not out:
            out.append(token)
            out_len = len(token)
    if out:
        yield ' '.join(out)


def escape(text):
    '''
    \   backslash
    `   backtick
    *   asterisk
    _   underscore
    {}  curly braces
    []  square brackets
    ()  parentheses
    #   hash mark
    +   plus sign
    -   minus sign (hyphen)
    .   dot
    !   exclamation mark
    |   kinovar
    +   wide
    '''
    # return regex.sub(r'([\\`\*_\{\}\[\]\(\)#\+\-\.\!])', r'\\\1', text)
    return regex.sub(r'([\\`\*_\|\+\{\}\[\]\(\)#])', r'\\\1', text)


def is_single_letter(text):
    '''is text a single letter with optional diacritics?'''
    return regex.match(r'\p{L}\p{M}*$', text) is not None