class Configuration:
    def __init__(self, s, i, a, b):
        self.s = s  # state of the parsing
        # (q - normal, b - back,f - final, e-error)
        self.i = i  # position of current symbol
        self.a = a  # working stack
        self.b = b  # input stack

    def is_head_nonterminal(self, grammar):
        input_stack = self.b
        if len(input_stack) > 0:
            symbol = input_stack.split(' ')[0]
            if symbol in grammar.N:
                return True
        return False

    def is_head_terminal(self, grammar):
        input_stack = self.b
        if len(input_stack) > 0:
            symbol = input_stack.split(' ')[0]
            if symbol in grammar.E:
                return True
            elif symbol == "epsilon":
                return True
        return False


    def __str__(self):
        if self.b is None:
            return "(" + self.s + ", " + str(self.i) + ", " + self.a + ", None" + ")"
        return "(" + self.s + ", " + str(self.i) + ", " + self.a + ", " + self.b + ")"
