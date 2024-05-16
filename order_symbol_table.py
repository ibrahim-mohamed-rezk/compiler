from collections import OrderedDict
import re

class OrderSymbolTable:
    def __init__(self):
        self.symbols = OrderedDict()
        self.counter = 1

    def add_variable(self, name, obj_address, variable_type, dimension, line_declaration):
        if name not in self.symbols:
            self.symbols[name] = {
                'counter': self.counter,
                'variable_name': name,
                'obj_address': obj_address,
                'type': variable_type,
                'dimension': dimension,
                'line_declaration': line_declaration,
                'line_reference': []
            }
            self.counter += 1

    def add_reference(self, name, line_reference):
        if name in self.symbols:
            self.symbols[name]['line_reference'].append(line_reference)

    def parse_code(self, code):
        lines = code.split('\n')
        current_line = 1

        for line in lines:
            # Match variable declaration
            match = re.match(r'^\s*(int|float|char|bool)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(?:=\s*(.*?))?;', line)
            if match:
                variable_type = match.group(1)
                variable_name = match.group(2)
                obj_address = hex(id(variable_name))
                dimension = 0
                if '[' in variable_name:
                    dimension = variable_name.count('[')
                    variable_name = variable_name.split('[')[0]
                self.add_variable(variable_name, obj_address, variable_type, dimension, current_line)

            # Match variable reference
            references = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=', line)
            for reference in references:
                self.add_reference(reference.strip(), current_line)

            current_line += 1

    def display_table(self):
        print("Order Symbol Table:")
        print("{:<8} {:<15} {:<15} {:<10} {:<10} {:<20} {:<20}".format('Counter', 'Variable Name', 'Obj Address', 'Type', 'Dimension', 'Line Declaration', 'Line Reference'))
        for symbol_name in sorted(self.symbols.keys()):
            symbol = self.symbols[symbol_name]
            print("{:<8} {:<15} {:<15} {:<10} {:<10} {:<20} {:<20}".format(symbol['counter'], symbol['variable_name'], symbol['obj_address'], symbol['type'], symbol['dimension'], symbol['line_declaration'], ', '.join(map(str, symbol['line_reference']))))

code = open('code.txt', 'r').read()
symbol_table = OrderSymbolTable()
symbol_table.parse_code(code)
symbol_table.display_table()
