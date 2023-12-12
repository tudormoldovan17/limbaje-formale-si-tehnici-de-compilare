from grammar import Grammar
from myparser import Parser

if __name__ == '__main__':

    # Read grammar from a file
    grammar1 = Grammar("grammar1.txt")
    grammar2 = Grammar("grammar2.txt")

    parser1 = Parser(grammar1)
    parser2 = Parser(grammar2)

    parser1.add_productions_to_file("( int + int )")
    parser2.add_productions_to_file("< and or and >")

    # print()
    # parser1.run_tests()
    grammar1.print_s()
    grammar1.print_terminals()
    grammar1.print_productions()
    grammar1.print_nonterminals()
    grammar1.print_productions_for_nonterminal("A")
    parser1.parser_output.print_to_screen()
    parser1.parser_output.print_to_file("final.txt")


