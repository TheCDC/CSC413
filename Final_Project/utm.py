import pprint
import json
DELIMITER_CHAR = '1'
DATA_CHAR = '0'
ALLOWED_CHARS = {DELIMITER_CHAR, DATA_CHAR}
given_input = '0010001010001001010100101110101001001001110'


def srl(n):
    """Return the set of integers [1, n]"""
    return set(range(0, len(n)))


def split_sections(s):
    return s.split(DELIMITER_CHAR * 3)


class UTM:

    def __init__(self, serialized):
        if set(serialized) != ALLOWED_CHARS:
            raise ValueError("Illegal characters! Allowed:{} but found {}".format(
                ALLOWED_CHARS, set(serialized)))
        machine, delta_section, input_tape = split_sections(serialized)

        properties = machine.split(DELIMITER_CHAR)
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
        self.start_state = len(properties[6]) - 1
        self.accept_state = len(properties[7]) - 1
        self.reject_state = len(properties[8]) - 1

        self.state = self.start_state

        self.tape = [len(x) - 1 for x in input_tape.split(DELIMITER_CHAR)]
        self.head_position = 0

        deltas = delta_section.split(DELIMITER_CHAR)
        if len(deltas) % 5 != 0:
            raise ValueError(
                """Length of deltas section must be multiple of 5!
Got {}""".format(len(deltas)))

        self.delta = dict()
        # slice delta section into definitions
        slices = [deltas[i:i + 5] for i in range(0, len(deltas), 5)]
        for delta in slices:
            # subtract one because '0' means state 0, not state 1.
            source_state = len(delta[0]) - 1
            # subtract 1 for the same reason
            read_symbol = len(delta[1]) - 1
            # ditto
            next_state = len(delta[2]) - 1
            # the symbol is sort of an id
            write_symbol = len(delta[3]) - 1
            # '00': right, '0': left?
            # convert to left = -1 and right = 1
            tape_direction = (len(delta[4]) - 1) * 2 - 1
            # define the delta function as a set of mappings from
            # a 2-tuple of (source_state, read_symbol)
            # to a 3 tuple of (next_state, write_symbol, tape_direction)
            self.delta.update({
                (source_state, read_symbol): (
                    next_state, write_symbol, tape_direction)
            })

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
Reject State:   {}
Tape:           {}""".format(
            self.states,
            self.tape_symbols,
            self.alphabet,
            self.eof_character,
            self.blank_character,
            self.num_transitions,
            self.start_state,
            self.accept_state,
            self.reject_state,
            self.tape,
        ))
        print("Deltas: ")
        pprint.pprint(self.delta)

    def advance(self):
        print("Advancing machine...{}")
        cur_char = self.tape[self.head_position]
        tup = (self.state, cur_char)
        try:
            result = self.delta[tup]
            print("Machine state: {}".format(tup))
            print("Applying delta tuple: {}".format(result))
        except KeyError:
            raise ValueError("""UTM has reached invalid configuration!
{}""".format(tup))
        next_state = result[0]
        write_symbol = result[1]
        tape_direction = result[2]
        self.tape[self.head_position] = write_symbol
        self.state = next_state
        if self.head_position == 0 and tape_direction == -1:
            raise ValueError("Machine attempted to go below index 0!")
        self.head_position += tape_direction
        # fill the tape with blanks as the machine goes along
        if self.head_position >= len(self.tape):
            self.tape.append(self.blank_character)


def main():
    u = UTM(given_input)
    u.summarize()
    u.advance()

if __name__ == '__main__':
    main()
