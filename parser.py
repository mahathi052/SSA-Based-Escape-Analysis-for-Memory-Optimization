from ast_nodes import *

def parse_code(code):
    lines = code.strip().split("\n")
    body = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if line.startswith("global"):
            continue

        # a = new   OR   a = new A();
        elif "= new" in line:
            var = line.split("=")[0].strip()
            body.append(NewObject(var))

        elif line.startswith("return"):
            var = line.split()[1]
            body.append(Return(var))

        elif line.startswith("call"):
            _, func, arg = line.split()
            body.append(Call(func, arg))

        elif "=" in line:
            left, right = line.split("=")
            body.append(Assign(left.strip(), right.strip()))

    return Function("user_func", body)
