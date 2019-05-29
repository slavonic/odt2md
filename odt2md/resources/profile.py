from odt2md.emphasis import MarkdownStyle

def profile(font, color, size, bold, italic):
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
