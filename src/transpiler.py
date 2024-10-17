import json
import sys

def transpile_code(input_code, name):
    lines = input_code.strip().splitlines()

    program = {
        "program": name,
        "global": "",
        "instructions": [
            {
                "instruction": "init",
                "code": [{}]
            },
            {
                "instruction": "execute",
                "code": [{}]
            }
        ],
        "code": []
    }

    context_stack = [program["code"]]

    def is_numeric(value):
        try:
            int(value.replace('"', ''))
            return True
        except:
            return False

    for line in lines:
        line = line.strip()
        if line.startswith("int "):
            _, var_name, _, value = line.split()
            value = value.strip().strip(';')
            v1 = True
            if is_numeric(value):
                v1 = False
                value = int(value)

            context_stack[-1].append({
                "type": "define",
                "code": {
                    "def": {
                        "variable": var_name,
                        "symbol": v1,
                        "value": not v1,
                        "content": value
                    },
                    "type": "int"
                }
            })
        elif line.startswith("print("):
            value = line[6:-1]
            context_stack[-1].append({
                "type": "print",
                "code": {
                    "value": value
                }
            })
        elif line.startswith("in("):
            var_name = line[3:-1]
            context_stack[-1].append({
                "type": "in",
                "code": {
                    "variable": var_name
                }
            })
        elif line.startswith("while"):
            condition = line[6:-2].strip()
            iteration_var, rel, count_var = condition.split()
            var1 = iteration_var.strip().replace('(','').replace(')','')
            var2 = count_var.strip().replace('(','').replace(')','')
            v1 = True
            v2 = True 
            if is_numeric(var1):
                v1 = False
                var1 = int(var1)
            if is_numeric(var2):
                v2 = False
                var2 = int(var2)
            while_block = {
                "type": "while",
                "condition": {
                    "variable1": {
                        "symbol": v1,
                        "content": var1
                    },
                    "variable2": {
                        "symbol": v2,
                        "content": var2
                    },
                    "relation": rel
                },
                "code": []
            }
            context_stack[-1].append(while_block)
            context_stack.append(while_block["code"])
        elif line.startswith("exit()"):
            context_stack[-1].append({
                "type": "exit"
            })
        elif line.endswith("}") and len(context_stack) > 1:
            context_stack.pop()
        elif line.startswith("if"):
            condition = line[3:-2].strip()
            iteration_var, rel, count_var = condition.split()
            var1 = iteration_var.strip().replace('(','').replace(')','')
            var2 = count_var.strip().replace('(','').replace(')','')
            v1 = True
            v2 = True 
            if is_numeric(var1):
                v1 = False
                var1 = int(var1)
            if is_numeric(var2):
                v2 = False
                var2 = int(var2)
            if_block = {
                "type": "if",
                "condition": {
                    "variable1": {
                        "symbol": v1,
                        "content": var1
                    },
                    "variable2": {
                        "symbol": v2,
                        "content": var2
                    },
                    "relation": rel
                },
                "code": []
            }
            context_stack[-1].append(if_block)
            context_stack.append(if_block["code"])
        elif line.startswith("#"):
            print("Skipping comment")
        else:
            if line.startswith("int "):
                _, var_name, _, value = line.split()
                v = True
                v1 = True
                if is_numeric(value):
                    value = int(value)
                    v = False
                if '"' in value:
                    v1 = False
                    v = False
                if '(' in value:
                    v = True
                if ')' in value:
                    v = True
                context_stack[-1].append({
                    "type": "define",
                    "code": {
                        "def": {
                            "variable": var_name,
                            "symbol": v,
                            "value": not v,
                            "content": value
                        },
                        "type": "int" if v1 else "String"
                    }
                })
            elif line.startswith("String "):
                _, var_name, _, value = line.split()
                v = True
                v1 = True
                if is_numeric(value):
                    value = int(value)
                    v = False
                if '"' in value:
                    v1 = False
                    v = False
                if '(' in value:
                    v = True
                if ')' in value:
                    v = True
                context_stack[-1].append({
                    "type": "define",
                    "code": {
                        "def": {
                            "variable": var_name,
                            "symbol": v,
                            "value": not v,
                            "content": value.replace('"', '')
                        },
                        "type": "int" if v1 else "String"
                    }
                })
            elif "=" in line:
                var_name, expr = line.split("=", 1)
                var_name = var_name.strip()
                expr = expr.strip().rstrip(';')

                if is_numeric(expr):
                    context_stack[-1].append({
                        "type": "define",
                        "code": {
                            "def": {
                                "variable": var_name,
                                "symbol": False,
                                "value": True,
                                "content": int(expr)
                            },
                            "type": "int"
                        }
                    })
                else:
                    if " + " in expr:
                        components = expr.split(" + ")
                        if len(components) == 2:
                            lhs, rhs = components
                            lhs = lhs.strip()
                            rhs = rhs.strip()
                            v1 = True
                            v2 = True

                            if '"' in lhs:
                                v1 = False
                            if '"' in rhs:
                                v2 = False
                            if (is_numeric(rhs)):
                                rhs = int(rhs)
                                v2 = False
                            if (is_numeric(lhs)):
                                lhs = int(lhs)
                                v1 = False


                            add_operations = {
                                "type": "add",
                                "code": {
                                    "variable1": {
                                        "symbol": v1,
                                        "content": lhs
                                    },
                                    "variable2": {
                                        "symbol": v2,
                                        "content": rhs
                                    },
                                    "result": var_name
                                }
                            }
                            context_stack[-1].append(add_operations)
                    else:
                        if '"' in expr:
                            context_stack[-1].append({
                                "type": "define",
                                "code": {
                                    "def": {
                                        "variable": var_name,
                                        "symbol": False,
                                        "value": True,
                                        "content": expr.replace('"', '')
                                    },
                                    "type": "String"
                                }
                            })
                        else:
                            context_stack[-1].append({
                                "type": "define",
                                "code": {
                                    "def": {
                                        "variable": var_name,
                                        "symbol": True,
                                        "value": False,
                                        "content": expr
                                    },
                                    "type": "int"
                                }
                            })
            elif "print(" in line:
                value = line[6:-1]
                context_stack[-1].append({
                    "type": "print",
                    "code": {
                        "value": value
                    }
                })

    return program

path = sys.argv[1]
with open(str(path)+'.xjs', 'r') as file:
        input_code = file.read()

transpiled_program = transpile_code(input_code, str(path)+'.xjs')
with open(str(path)+'.json', 'w') as file:
    file.write(json.dumps(transpiled_program, indent=4))
