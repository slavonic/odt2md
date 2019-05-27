from odt2md.util import escape

def test():
    assert escape('Hello!') == r'Hello!'
    assert escape('[1](2)\\') == r'\[1\]\(2\)\\'
