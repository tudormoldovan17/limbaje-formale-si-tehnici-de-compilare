class ParserOutput:
    def __init__(self):
        self.parsing_tree = []

    def add_to_tree(self, action):
        self.parsing_tree.append(action)

    def transform_parsing_tree(self):
        # Transforming the list-based parsing tree into a string representation
        return ' '.join(self.parsing_tree)

    def print_to_screen(self):
        print("Parsing Tree:", self.transform_parsing_tree())

    def print_to_file(self, file_name):
        with open(file_name, "w") as file:
            file.write("Parsing Tree: " + self.transform_parsing_tree())
