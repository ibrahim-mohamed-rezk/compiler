
import re

code = open("code.txt", "r").read()

lines = code.split("\n")

for line_num , line in enumerate(lines, start=1):
    if not line.strip():
        continue

    match_dec = re.match(r'^\s*(int|float|char|bool)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(?:=\s*(.*?))?;', line)
    
    if match_dec :
        v_type = match_dec.group(1)
        v_name = match_dec.group(2)
        v_value = match_dec.group(3)
        print("Declaration")
        print(v_name)
        print(v_type)
        print(v_value)
        print(";")
    else:
        match_assign = re.match(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.*)', line)
        if match_assign:
            v_name = match_assign.group(1)
            v_value = match_assign.group(2)
            print("Assignment")
            print(v_name)
            print(v_value)
            print(";")