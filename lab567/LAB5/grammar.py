class Grammar:
    def __init__(self, file_name):
        self.N = set()  # non-terminals
        self.E = set()  # terminals
        self.P = list()
        self.S = ""
        self.file_name = file_name
        self.read_from_file(file_name)

    def read_from_file(self, file_name):
        try:
            file = open(file_name, 'r')
            lines = file.readlines()

            idx = 0
            for line in lines:

                # First line is N
                if idx == 0:
                    tokens = line.split("=", 1)
                    if len(tokens) != 2:
                        raise ValueError("Wrong file input")
                    self.N = tokens[1].replace('\n', '').replace('{', '').replace('}', '').split(' ')
                    while "" in self.N:
                        self.N.remove("")

                elif idx == 1:
                    tokens = line.split("=", 1)
                    if len(tokens) != 2:
                        raise ValueError("Wrong file input")
                    self.E = tokens[1].replace('\n', '').replace('{', '').replace('}', '').split(' ')
                    while "" in self.E:
                        self.E.remove("")

                elif idx == 2:
                    tokens = line.split("=", 1)
                    if len(tokens) != 2:
                        raise ValueError("Wrong file input")
                    self.S = tokens[1].replace('\n', '').replace('{', '').replace('}', '').split(' ')
                    while "" in self.S:
                        self.S.remove("")

                elif idx == 3:
                    pass

                else:
                    if line == "}":
                        idx += 1
                        continue
                    tokens = line.split("->")
                    if len(tokens) != 2:
                        raise ValueError("Wrong file input")
                    production_right = tokens[1].replace('\n', '').replace('\t', '').replace('{', '').replace('}', '').split(' ')
                    while "" in production_right:
                        production_right.remove("")
                    # print(production_right)
                    production_left = tokens[0].replace(' ', '').replace('\t', '').replace('{', '').replace('}', '')
                    self.P.append((production_left, production_right))

                idx += 1

        except Exception as ex:
            print(ex)
            exit(0)

    def print_nonterminals(self):
        print("Non Terminals:")
        print(self.N)

    def print_terminals(self):
        print("Terminals:")
        print(self.E)

    def print_s(self):
        print("S = ",end='')
        print(self.S)

    def print_productions(self):
        print("Productions:")
        for production in self.P:
            print(production[0] + " -> " + str(production[1]))

    def print_productions_for_nonterminal(self, nt):
        print("Productions for nonterminal " + nt + ":")
        productions = self.prod_for_nonterminals(nt)
        for production in productions:
            print(production[0] + " -> " + str(production[1]))

    def prod_for_nonterminals(self, nt):
        my_list = list()
        for production in self.P:
            if production[0] == nt:
                my_list.append(production)
        return my_list
