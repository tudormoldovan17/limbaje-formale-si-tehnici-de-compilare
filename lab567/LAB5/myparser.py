from ParserOutput import ParserOutput
from configuration import Configuration


class Parser:

    def __init__(self, grammar):
        self.config = Configuration('q', 1, 'epsilon', 'S')
        self.grammar = grammar
        self.another_try_index = 0
        self.file_name = grammar.file_name.replace('.txt', '') + "_out.txt"
        self.file = open(self.file_name, "w")
        self.parser_output = ParserOutput()
        # s = state of the parsing (q, b, f, e)

    def get_head(self):
        if ' ' in self.config.b:
            return self.config.b.split(' ')[0]
        return self.config.b

    def get_remaining(self):
        if ' ' in self.config.b:
            return self.config.b.split(' ', 1)[1]
        return ""

    def get_head_a(self):
        if ' ' in self.config.a:
            return self.config.a.split(' ')[-1]
        return self.config.a

    def get_remaining_a(self):
        if ' ' in self.config.a:
            items = self.config.a.split(' ')
            items.pop()
            string = ""
            for item in items:
                string += ' ' + item
            return string[1:]
        return ""

    def check_head(self, seq):
        index = self.config.i - 1
        items_list = seq.split(' ')
        if index >= len(items_list):
            return False
        if items_list[index] == self.get_head():
            return True
        return False

    def get_production(self, nt, idx):
        productions = self.grammar.prod_for_nonterminals(nt)
        if len(productions) == 0:
            return None
        string = ""
        for item in productions[idx][1]:
            string += ' ' + item
        return string[1:]

    def out_of_productions(self, nt, idx):
        productions = self.grammar.prod_for_nonterminals(nt)
        if idx == len(productions):
            return True
        return False

    def expand(self):
        # When the head of the input stack is a nonterminal
        self.parser_output.add_to_tree("expand |-- ")
        self.file.write("expand |-- ")
        if self.get_head() is None:
            self.file.write(self.config.b)
            return None
        if self.config.a == 'epsilon':
            self.config.a = self.get_head() + " 1"
        else:
            self.config.a += ' ' + self.get_head() + " 1"

        prod = self.get_production(self.get_head(), 0)
        if self.get_remaining() is None:
            if prod == 'epsilon':
                prod = ''
            self.config.b = prod
        elif prod == 'epsilon':
            self.config.b = self.get_remaining()
        else:
            self.config.b = prod + ' ' + self.get_remaining()
        self.parser_output.add_to_tree(str(self.config) + '\n')
        self.file.write(str(self.config) + '\n')

    def advance(self):
        self.parser_output.add_to_tree("advance |-- ")
        self.file.write("advance |-- ")
        if self.get_head() is None:
            return
        self.config.a += ' ' + self.get_head()

        if self.get_remaining() is None:
            self.config.b = ""
        else:
            self.config.b = self.get_remaining()

        self.config.i += 1
        self.file.write(str(self.config) + '\n')
        self.parser_output.add_to_tree(str(self.config) + '\n')

    def mom_insuccess(self):
        self.parser_output.add_to_tree("mom ins |-- ")
        self.file.write("mom ins |-- ")
        self.config.s = 'b'
        self.file.write(str(self.config) + '\n')
        self.parser_output.add_to_tree(str(self.config) + '\n')

    def back(self):
        self.parser_output.add_to_tree("back |-- ")
        self.file.write("back |-- ")
        if self.get_head_a() is None:
            return
        self.config.b = self.get_head_a() + ' ' + self.config.b

        if self.get_remaining_a() is None:
            self.config.a = ""
        else:
            self.config.a = self.get_remaining_a()

        self.config.i -= 1
        self.file.write(str(self.config) + '\n')
        self.parser_output.add_to_tree(str(self.config) + '\n')

    def another_try(self):

        if self.config.i == 1 and len(self.config.a) == 0:
            self.config.s = 'e'
            return
        self.parser_output.add_to_tree("ant try |-- ")
        self.file.write("ant try |-- ")
        index = int(self.get_head_a())

        self.config.a = self.get_remaining_a()
        nt = self.get_head_a()

        if self.out_of_productions(nt, index):
            self.config.a = self.get_remaining_a()
            self.config.b = nt + ' ' + self.get_remaining()
        else:
            prod = self.get_production(nt, index)
            prev_prod_nr_of_elements = 1
            if index > 0:
                prev_prod_nr_of_elements = self.get_production(nt, index - 1).count(' ') + 1
            for x in range(prev_prod_nr_of_elements):
                self.config.b = self.get_remaining()
            if prod != 'epsilon':
                self.config.b = prod + ' ' + self.config.b
            self.config.a += ' ' + str(index + 1)
            self.config.s = 'q'

        self.file.write(str(self.config) + '\n')
        self.parser_output.add_to_tree(str(self.config) + '\n')

    def success(self):
        self.parser_output.add_to_tree("success |-- ")
        self.file.write("success |-- ")
        self.config.s = 'f'
        self.file.write(str(self.config) + '\n')
        self.parser_output.add_to_tree(str(self.config) + '\n')

    def algorithm(self, sequence):
        n = len(sequence.split(' '))
        self.config = Configuration('q', 1, 'epsilon', 'S')
        self.file = open(self.file_name, "a")
        self.file.write(str(self.config) + '\n')
        self.parser_output.add_to_tree(str(self.config) + '\n')
        while self.config.s != 'f' and self.config.s != 'e':
            if self.config.s == 'q':
                if self.config.i == n + 1 and len(self.config.b) == 0:
                    self.success()
                elif self.config.is_head_nonterminal(self.grammar):  # head of the input stack is a nonterminal
                    self.expand()
                elif self.config.is_head_terminal(self.grammar) and self.check_head(
                        sequence):  # head of input stack is a TERMINAL
                    self.advance()
                else:
                    self.mom_insuccess()  # head of stack is a terminal != a current symbol from input

            # back
            elif self.config.s == 'b':
                # print("head: " + self.get_head_a())
                # print("terminals: " + str(self.grammar.E))
                if self.get_head_a() in self.grammar.E:
                    self.back()
                else:
                    self.another_try()

        if self.config.s == 'e':
            return ''
        else:
            return self.build_string_of_productions()

# 8.5 9.5 6 8 8 9.5 9.5 10 10 10
    def build_string_of_productions(self):
        items = self.config.a.split(' ')
        length = len(items)
        string = ""
        for i in range(length - 1):
            if items[i] in self.grammar.N:
                string += items[i] + items[i + 1] + ' '
                i += 1
        return string

    def add_productions_to_file(self, sequence):
        self.algorithm(sequence)
        string_of_prod = self.build_string_of_productions()
        self.file.close()
        self.file = open(self.file_name, "a")
        if string_of_prod != '':
            self.file.write("Sequence accepted\n")
            self.file.write("String of productions: ")
            self.parser_output.add_to_tree("String of productions: " + string_of_prod)
            self.file.write(string_of_prod)
            self.file.close()
        else:
            self.file.write("Sequence not accepted")
            self.file.close()

    def run_tests(self):
        f = open("tests_result.txt", "w")
        # We know that our grammar generates correct arithmetic sequences of additions and productions
        # So, in case we have a readable, syntactically correct arithmetic sequence, the test should pass
        # Otherwise, the test will fail

        # CORRECT
        f.write(self.run_test("( int + int )"))
        f.write(self.run_test("( int * ( int + int ) )"))
        f.write(self.run_test("( int * ( int + int + int )"))
        f.write(self.run_test("( int * ( int + int ) )"))
        f.write(self.run_test("( int + ( int * int ) )"))
        f.write(self.run_test("( int * int + int )"))
        f.write(self.run_test("( ( int + int ) + int * int + int )"))

        # WRONG
        f.write(self.run_test(""))
        f.write(self.run_test(" int + int "))
        f.write(self.run_test("( a + int )"))
        f.write(self.run_test("( + int )"))
        f.write(self.run_test("( )"))
        f.write(self.run_test("( + + )"))
        f.write(self.run_test("( ( int + int ) * int * int + int )"))

    def run_test(self, sequence):
        string_of_prod = self.algorithm(sequence)
        if string_of_prod != '':
            return sequence + " --> CORRECT --> " + string_of_prod + "\n"
        else:
            return sequence + " --> WRONG" + "\n"
