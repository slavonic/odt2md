from odt2md.util import is_single_letter

def test():
    assert is_single_letter('Ѡ҆') == True
    assert is_single_letter('1') == False
    assert is_single_letter('AB') == False