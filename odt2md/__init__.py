__version__      = '0.0.13'
__author__       = 'Mike Kroutikov'
__author_email__ = 'pgmmpk@gmail.com'
__description__  = 'Tools to convert LibreOffice document to Church-Slavonic Markdown flavor'
__keywords__     = 'odt, LibreOffice, Markdown'
__url__          = 'https://github.com/slavonic/odt2md'

import os

def res(*av):
    return os.path.join(
        os.path.dirname(__file__),
        'resources',
        *av
    )