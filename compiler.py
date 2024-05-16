import re
from tabulate import tabulate

TOKEN_TYPES = {
    'KEYWORD': r'\b(print|int|float|char)\b',
    'NUMBER': r'\b\d+(\.\d+)?\b',
    'STRING': r'"[^"]*"',
    'ID': r'\b[a-zA-Z_][a-zA-Z0-9_]*\b',
    'OP': r'[-+*/=]',
    'PAREN': r'[\(|\)|\{|\}]',
    'SEMICOLON': r';',
}


def read_code_from_file(filename):
    try:
        with open(filename, 'r') as file:
            code = file.read()
        return code
    except Exception as e:
        print(f"Error reading file: {e}")
        return None
# lexer
def tokenize(code):
    tokens = []
    patterns = '|'.join(f'(?P<{type}>{pattern})' for type, pattern in TOKEN_TYPES.items())
    for match in re.finditer(patterns, code):
        token_type = match.lastgroup
        token_value = match.group(token_type)
        tokens.append((token_type, token_value))
    return tokens


# parser
variables = {}
errors = []
def parse(code):
    lines = code.split('\n')
    for line_num, line in enumerate(lines, start=1):
        if not line.strip():
            continue  # Skip empty lines

        # Match variable declaration
        match_declaration = re.match(r'^\s*(int|float|char|bool)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(?:=\s*(.*?))?;', line)
        if match_declaration:
            variable_type = match_declaration.group(1)
            variable_name = match_declaration.group(2)
            if match_declaration.group(3) is not None:
                expression = match_declaration.group(3).strip()  # Get the value expression
                try:
                    value = evaluate_expression(line_num, expression)
                    if variable_name in variables:
                        errors.append(f"Error in line {line_num}: Variable '{variable_name}' redeclaration")
                    variables[variable_name] = {'type': variable_type, 'value': value}
                except Exception as e:
                    errors.append(f"Error in line {line_num}: {e}")
            else:
                if variable_name in variables:
                    errors.append(f"Error in line {line_num}: Variable '{variable_name}' redeclaration")
                variables[variable_name] = {'type': variable_type, 'value': None}
        else:
            # Match variable assignment with arithmetic expression
            match_assignment = re.match(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.*?);', line)
            if match_assignment:
                variable_name = match_assignment.group(1)
                expression = match_assignment.group(2).strip()  # Get the expression
                if variable_name not in variables:
                    errors.append(f"Error in line {line_num}: Variable '{variable_name}' not declared")
                try:
                    value = evaluate_expression(line_num, expression)
                    variables[variable_name]['value'] = value
                except Exception as e:
                    errors.append(f"Error in line {line_num}: {e}")
            else:
                errors.append(f"Error in line {line_num}: Invalid syntax")

def evaluate_expression(line_num, expression):
    local_vars = variables.copy()
    # Replace variable names in the expression with their values
    for var_name, var_info in variables.items():
        local_vars[var_name] = var_info['value']

    try:
        # Evaluate the expression with updated local variables
        return eval(expression, {}, local_vars)
    except Exception as e:
        raise ValueError(f"Error evaluating expression in line {line_num}: {e}")

def display_variables():
    print("Variable Table:")
    print("{:<15} {:<15}".format('Variable Name', 'Value'))
    for name, info in variables.items():
        print("{:<15} {:<15}".format(name, info['value']))



# parse tree
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





def main():
    code = read_code_from_file("code.txt")
    if code is not None:
        # print Tokenization
        tokens = tokenize(code)
        print("Number of tokens:", len(tokens))
        print(tabulate(tokens, headers=['Lexeme', 'Token'], tablefmt='grid'))
        print("\n")
        print("\n")

        # print parser
        parse(code)
        print("Errors:")
        for error in errors:
            print(error)
        print("Variable Table:")
        print("{:<15} {:<15}".format('Variable Name', 'Value'))
        for name, info in variables.items():
            print("{:<15} {:<15}".format(name, info['value']))
        print("\n")
        print("\n")

        # print parse tree
        root = parse_program(tokens)
        print_tree(root)





if __name__ == '__main__':
    main()
