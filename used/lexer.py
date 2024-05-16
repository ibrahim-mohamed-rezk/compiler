import re
from tabulate import tabulate

class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.tokenize()

    def tokenize(self):
        patterns = {
            'KEYWORD': r'(int|float|char)',
            'IDENTIFIER': r'[a-zA-Z_][a-zA-Z0-9_]*',
            'NUMBER': r'\d+',
            'OPERATOR': r'[\+\-\*/]',
            'ASSIGNMENT': r'=',
            'SEMICOLON': r';',
            'STRING_LITERAL': r'"[^"]*"|\'[^\']*\''
        }

        # Combine all patterns into one regular expression
        combined_pattern = '|'.join(f'(?P<{token_type}>{pattern})' for token_type, pattern in patterns.items())

        # Tokenize the code
        self.tokens = []
        for match in re.finditer(combined_pattern, self.code):
            token_type = match.lastgroup
            token_value = match.group(token_type)
            # Update token type to 'STRING_LITERAL' if it matches the string literal pattern
            if token_type == 'IDENTIFIER' and (token_value.startswith('"') or token_value.startswith("'")):
                token_type = 'STRING_LITERAL'
            self.tokens.append((token_value, token_type))

        print("Number of tokens:", len(self.tokens))
        print(tabulate(self.tokens, headers=['Lexeme', 'Token'], tablefmt='grid'))

code = open('code.txt', 'r').read()
lexer = Lexer(code)