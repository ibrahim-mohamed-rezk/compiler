def calculate_first(grammar):
    first_sets = {}  # Dictionary to store First sets for each non-terminal

    # Initialize First sets with empty sets for each non-terminal
    for non_terminal in grammar.non_terminals:
        first_sets[non_terminal] = set()

    # Iterate through each production rule
    for rule in grammar.rules:
        non_terminal = rule.non_terminal
        symbols = rule.symbols

        # Call a recursive function to compute First set for the current rule
        compute_first(first_sets, symbols)

    return first_sets

def compute_first(first_sets, symbols):
    # Implement recursive logic to compute First set for symbols
    pass

# Example usage
class ProductionRule:
    def __init__(self, non_terminal, symbols):
        self.non_terminal = non_terminal
        self.symbols = symbols

class Grammar:
    def __init__(self, rules, non_terminals):
        self.rules = rules
        self.non_terminals = non_terminals

# Example grammar
rules = [
    ProductionRule('A', ['a', 'B', 'c']),
    ProductionRule('B', ['b', 'C']),
    # Add more production rules here
]

non_terminals = ['A', 'B', 'C']  # List of non-terminal symbols

grammar = Grammar(rules, non_terminals)

first_sets = calculate_first(grammar)
print(first_sets)
