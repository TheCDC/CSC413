DELIMITER_CHAR = '1'
DATA_CHAR = '0'
given_input = '0010001010001001010100101110101001001001110'


def srl(n):
    """Return the set of integers [1, n]"""
    return set(range(1, 1 + len(n)))


def split_sections(s):
    return s.split(DELIMITER_CHAR * 3)


class UTM:

    def __init__(self, serialized):
        machine, delta_section, input_tape = split_sections(serialized)

        properties = machine.split('1')
        # validate that all the symbol sections are there
        if len(properties) != 9:
            raise ValueError(
                """Missing machine properties!
                Expected 9, got {}
                {}""".format(len(properties), properties))

        self.states = srl(properties[0])
        self.tape_symbols = srl(properties[1])
        self.alphabet = srl(properties[2])
        self.eof_character = len(properties[3])
        self.blank_character = len(properties[4])
        self.num_transitions = len(properties[5])
        self.start_state = len(properties[6])
        self.accept_state = len(properties[7])
        self.reject_state = len(properties[8])

        deltas = delta_section.split(DELIMITER_CHAR)
        if len(deltas) % 5 != 0:
            raise ValueError(
                """Length of deltas section must be multiple of 5!
Got {}""".format(len(deltas)))

    def summarize(self):
        print("""UTM Instance
States:         {}
Tape Symbols:   {}
Alphabet:       {}
EOF:            {}
Blank:          {}
Num Deltas:     {}
Start State:    {}
Accept State:   {}
Reject State:   {}""".format(
            self.states,
            self.tape_symbols,
            self.alphabet,
            self.eof_character,
            self.blank_character,
            self.num_transitions,
            self.start_state,
            self.accept_state,
            self.reject_state,
        ))


def main():
    u = UTM(given_input)
    u.summarize()

if __name__ == '__main__':
    main()
