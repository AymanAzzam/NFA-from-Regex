from State import State


class Block:

    def __init__(self, character=None, a=None, b=None, operator=None):
        self.character = character
        self.A = a
        self.B = b
        self.operator = operator

    def json_output(self):
        json_text = '{\n' \
                    '   "startingState": "S0",\n'
        json_text += self.json(is_terminating=True)[1]
        json_text = json_text[:-2] + "\n}"
        return json_text

    def json(self, starting_state=0, end_state_given=-1, is_terminating=False):
        if self.character is not None:
            s0 = State(starting_state)
            s0.connect(self.character, starting_state + 1)
            s1 = State(starting_state + 1, is_terminating)
            last_created_state = self.put_end_state(starting_state + 1, s1, end_state_given, is_terminating)
            return last_created_state, s0.json() + s1.json()
        elif self.operator == '.':
            last_created_state, a_json = self.A.json(starting_state)
            last_created_state, b_json = self.B.json(last_created_state, end_state_given, is_terminating)
            return last_created_state, a_json + b_json
        elif self.operator == "+":
            left_state = State(starting_state)
            right_state = State(starting_state + 1, is_terminating)
            e1, a_json = self.A.json(starting_state + 2, right_state.number)
            e2, b_json = self.B.json(e1 + 1, right_state.number)
            left_state.connect("Epsilon", starting_state + 2)
            left_state.connect("Epsilon", e1 + 1)
            last_created_state = self.put_end_state(e2, right_state, end_state_given, is_terminating)
            return last_created_state, left_state.json() + a_json + b_json + right_state.json()
        elif self.operator == "*":
            left_state = State(starting_state)
            right_state = State(starting_state + 1, is_terminating)
            e1, a_json = self.A.json(starting_state + 2, [right_state.number, left_state.number])
            left_state.connect("Epsilon", starting_state + 2)
            left_state.connect("Epsilon", right_state.number)
            last_created_state = self.put_end_state(e1, right_state, end_state_given, is_terminating)
            return last_created_state, left_state.json() + a_json + right_state.json()

    def put_end_state(self, last_created_state_number, end_state, end_state_given, is_terminating):
        if end_state_given != -1:
            if type(end_state_given) == list:
                for s in end_state_given:
                    end_state.connect("Epsilon", s)
            else:
                end_state.connect("Epsilon", end_state_given)
            return last_created_state_number
        elif not is_terminating:
            end_state.connect("Epsilon", last_created_state_number + 1)
            return last_created_state_number + 1