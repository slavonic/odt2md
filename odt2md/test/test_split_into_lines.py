from odt2md.util import split_into_lines


def test():

    result = list(split_into_lines('a b c d e f g h k', max_line_width=5))
    assert result == ['a b c', 'd e f', 'g h k']

def test_long_word():
    result = list(split_into_lines('a b c d1234567890 e f g h k', max_line_width=5))
    assert result == ['a b c', 'd1234567890', 'e f g', 'h k']
