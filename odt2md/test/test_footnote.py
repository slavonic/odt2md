from odt2md.odt2md import odt2md
import tempfile
import zipfile
from . import res


def test_toc_mark():
    '''should not crash'''
    with tempfile.TemporaryDirectory() as d:
        md_zip = f'{d}/footnote_test.zip'
        odt2md(res('footnote_test.odt'), md_zip)
        with zipfile.ZipFile(md_zip) as z:
            content = z.read('content.md')

    model = b'''\
Some document with a footnote[^1]

[^1]: Hello, world!

Let me also try to style a footnote***[^2]***

[^2]: **Bold footnote**

'''
    if content != model:
        print(model)
        print(content)
        assert False

