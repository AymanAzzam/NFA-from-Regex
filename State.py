class State:

    def __init__(self, number, is_terminating=False):
        self.number = number
        self.is_terminating = is_terminating
        self.input_to_states = {}

    def connect(self, input_character, state_number):
        if input_character in self.input_to_states:
            self.input_to_states[input_character].append(state_number)
        else:
            self.input_to_states[input_character] = [state_number]

    def json(self):
        json = \
            '"S{}": {{\n' \
            '   "isTerminatingState": {},\n'.format(self.number, str(self.is_terminating).lower())
        for input_character, states in self.input_to_states.items():
            json += '   "{}": [\n'.format(input_character)
            for i, state in enumerate(states):
                json += '       "S{}"'.format(state)
                json += ',\n' if i != len(states) - 1 else "\n"
            json += '   ]\n'
        json += '}\n'
        return json