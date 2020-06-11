from odt2md.odt2md import odt2md
import tempfile
from . import res


def test_toc_mark():
    '''should not crash'''
    with tempfile.TemporaryDirectory() as d:
        md_zip = f'{d}/0701.zip'
        odt2md(res('0701.odt'), md_zip)
