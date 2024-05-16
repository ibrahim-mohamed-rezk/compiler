class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, node):
        self.children.append(node)

def parse_program(tokens):
    root = TreeNode("program")
    root.add_child(parse_declaration_list(tokens))
    return root

def parse_declaration_list(tokens):
    node = TreeNode("declaration_list")
    while tokens:
        node.add_child(parse_declaration(tokens))
    return node

def parse_declaration(tokens):
    node = TreeNode("declaration")
    node.add_child(parse_type_specifier(tokens))
    node.add_child(parse_identifier_list(tokens))
    return node

def parse_type_specifier(tokens):
    return TreeNode(tokens.pop(0)[1])  # type specifier

def parse_identifier_list(tokens):
    node = TreeNode("identifier_list")
    while tokens and tokens[0][1] != ';':
        node.add_child(TreeNode(tokens.pop(0)[0]))  # identifier
        if tokens and tokens[0][1] == ',':
            tokens.pop(0)  # consume the ','
    return node

def print_tree(node, indent="", last=True):
    print(indent, end="")
    if last:
        print("└──", end="")
        indent += "   "
    else:
        print("├──", end="")
        indent += "│  "
    print(node.value)
    
    children_count = len(node.children)
    for index, child in enumerate(node.children):
        print_tree(child, indent, index == children_count - 1)

from  used.lexer import *
code = open('code.txt', 'r').read()
lexer = Lexer(code)
tokens = lexer.tokens
root = parse_program(tokens)
print_tree(root)