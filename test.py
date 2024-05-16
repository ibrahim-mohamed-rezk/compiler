import re

code = open("code.txt", "r").read()

TYPES = {
    'keyword': r'\b(print|int|float|if|char)\b',
    'number': r'\b\d+\b',
    'string': r'"[^"]*"',
    'id': r'\b[a-zA-Z][a-zA-Z0-9]*\b'
}

tokens = []
patterns = '|'.join(f'(?P<{type}>{pattern})' for type, pattern in TYPES.items())
patterns = '|'.join(f'(?P<{type}>{pattern})' for type, pattern in TYPES.items())
for match in re.finditer(patterns, code):
    t_type = match.lastgroup
    t_value = match.group(t_type)
    tokens.append((t_type, t_value))

print(tokens)


print("\n")

# lines = code.split("\n")

# for line_num , line in enumerate(lines, start=1):
#     if not line.strip():
#         continue

#     match_dec = re.match(r'^\s*(int|float|char|bool)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(?:=\s*(.*?))?;', line)
    
#     if match_dec :
#         v_type = match_dec.group(1)
#         v_name = match_dec.group(2)
#         v_value = match_dec.group(3)
#         print("Declaration")
#         print(v_name)
#         print(v_type)
#         print(v_value)
#         print(";")
#     else:
#         match_assign = re.match(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.*)', line)
#         if match_assign:
#             v_name = match_assign.group(1)
#             v_value = match_assign.group(2)
#             print("Assignment")
#             print(v_name)
#             print(v_value)
#             print(";")
