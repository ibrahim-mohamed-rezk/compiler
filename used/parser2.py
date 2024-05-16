import re

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

def display_errors():
    print("Errors:")
    for error in errors:
        print(error)


code = open('code.txt', 'r').read()
parser = parse(code)

display_errors()
display_variables()