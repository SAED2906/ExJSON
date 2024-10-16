import json
import re
import sys

variables = {}
symbol_types = {}

def printf(code_block):
    out_code = code_block.get("code", {})
    out_value = out_code.get("value")

    pattern = r"\$\{([a-zA-Z_][a-zA-Z0-9_]*)\}"
    result = re.sub(pattern, lambda match: str(variables.get(match.group(1), match.group(0))), out_value)
    print(result.replace('\\n', '\n').replace('\"', ''))

def add(code_block):
    add_code = code_block.get("code", {})
    c_var1 = add_code.get('variable1', {})
    c_var2 = add_code.get('variable2', {})
    result = add_code.get('result')

    var1 = 0
    var2 = 0

    if c_var1.get('symbol'):
        var1 = variables[c_var1.get('content')]
        if symbol_types[c_var1.get('content')] == "int":
            var1 = int(var1)
    else:
        var1 = c_var1.get('content')

    if c_var2.get('symbol'):
        var2 = variables[c_var2.get('content')]
        if symbol_types[c_var2.get('content')] == "int":
            var2 = int(var2)
    else:
        var2 = c_var2.get('content')

    variables[result] = var1 + var2

def define(code_block):
    define_code = code_block.get("code", {})
    define_def = define_code.get("def", {})
    if define_def.get('value'):
        variables[define_def.get('variable')] = define_def.get('content')
        symbol_types[define_def.get('variable')] = define_code.get("type")
    elif define_def.get('symbol'):
        variables[define_def.get('variable')] = variables[define_def.get('content')]
        symbol_types[define_def.get('variable')] = define_code.get("type")

def inp(code_block):
    in_code = code_block.get("code", {})
    value = input()
    if symbol_types[in_code.get('variable')] == "int":
        value = int(value)
    if symbol_types[in_code.get('variable')] == "String":
        value = str(value)

    variables[in_code.get('variable')] = value

def whileloop(code_block):
    condition = code_block.get("condition", {})
    c_var1 = condition.get('variable1', {})
    c_var2 = condition.get('variable2', {})
    relation = condition.get('relation')

    var1 = 0
    var2 = 0

    if c_var1.get('symbol'):
        var1 = variables[c_var1.get('content')]
        if symbol_types[c_var1.get('content')] == "int":
            var1 = int(var1)
    else:
        var1 = c_var1.get('content')

    if c_var2.get('symbol'):
        var2 = variables[c_var2.get('content')]
        if symbol_types[c_var2.get('content')] == "int":
            var2 = int(var2)
    else:
        var2 = c_var2.get('content')
    
    if relation == "<":
        while (var1 < var2):
            cbs = code_block.get('code', {})
            sub_def(cbs);

            var1 = variables[c_var1.get('content')]
            if symbol_types[c_var1.get('content')] == "int":
                var1 = int(var1)

            var2 = variables[c_var2.get('content')]
            if symbol_types[c_var2.get('content')] == "int":
                var2 = int(var2)

    elif relation == "<=":
        while (var1 <= var2):
            cbs = code_block.get('code', {})
            sub_def(cbs);

            var1 = variables[c_var1.get('content')]
            if symbol_types[c_var1.get('content')] == "int":
                var1 = int(var1)

            var2 = variables[c_var2.get('content')]
            if symbol_types[c_var2.get('content')] == "int":
                var2 = int(var2)
    elif relation == ">":
        while (var1 > var2):
            cbs = code_block.get('code', {})
            sub_def(cbs);

            var1 = variables[c_var1.get('content')]
            if symbol_types[c_var1.get('content')] == "int":
                var1 = int(var1)

            var2 = variables[c_var2.get('content')]
            if symbol_types[c_var2.get('content')] == "int":
                var2 = int(var2)
    elif relation == ">=":
        while (var1 >= var2):
            cbs = code_block.get('code', {})
            sub_def(cbs);

            var1 = variables[c_var1.get('content')]
            if symbol_types[c_var1.get('content')] == "int":
                var1 = int(var1)

            var2 = variables[c_var2.get('content')]
            if symbol_types[c_var2.get('content')] == "int":
                var2 = int(var2)
    elif relation == "==":
        while (var1 == var2):
            cbs = code_block.get('code', {})
            sub_def(cbs);

            var1 = variables[c_var1.get('content')]
            if symbol_types[c_var1.get('content')] == "int":
                var1 = int(var1)

            var2 = variables[c_var2.get('content')]
            if symbol_types[c_var2.get('content')] == "int":
                var2 = int(var2)
    elif relation == "!=":
        while (var1 != var2):
            cbs = code_block.get('code', {})
            sub_def(cbs);

            var1 = variables[c_var1.get('content')]
            if symbol_types[c_var1.get('content')] == "int":
                var1 = int(var1)

            var2 = variables[c_var2.get('content')]
            if symbol_types[c_var2.get('content')] == "int":
                var2 = int(var2)


def sub_def(code_blocks):
    for code_block in code_blocks:
        code_type = code_block.get("type")

        if code_type == "define":
            define(code_block)

        elif code_type == "in":
            inp(code_block)

        elif code_type == "print":
            printf(code_block)

        elif code_type == "add":
            add(code_block)

        elif code_type == "while":
            whileloop(code_block)

        elif code_type == "exit":
            print("Exit instruction found.")
            exit(0)

def execute():
    path = sys.argv[1]
    with open(str(path) + '.json', 'r') as file:
        data = json.load(file)

    print("Program:", data.get("program"))
    
    code_blocks = data.get("code", [])
    sub_def(code_blocks)
    

if __name__ == "__main__":
    # main()
    execute()
