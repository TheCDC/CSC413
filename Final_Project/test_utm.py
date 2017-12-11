from utm import UTM, split_sections, given_input


def test_split_sections():
    ss = split_sections(given_input)
    assert len(ss) == 3
    assert ss[0] == '001000101000100101010010'
    assert ss[1] == '010100100100'
    assert ss[2] == '0'


def test_utm():
    u = UTM(given_input)
    assert u.states == {0, 1}
    assert len(u.tape_symbols) == 3
    assert len(u.alphabet) == 1
    assert u.eof_character == 3
    assert u.blank_character == 2
    assert u.num_transitions == 1
    assert u.start_state == 0
    assert u.accept_state == 1
    assert u.reject_state == 0
