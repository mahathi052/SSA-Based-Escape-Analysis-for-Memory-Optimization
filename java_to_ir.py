import re

def java_to_pseudo(java_code):
    ir = []

    for line in java_code.splitlines():
        line = line.strip()

        # new object
        m = re.match(r".* (\w+) = new \w+.*", line)
        if m:
            ir.append(f"{m.group(1)} = new Object")
            continue

        # return
        m = re.match(r"return (\w+)", line)
        if m:
            ir.append(f"return {m.group(1)}")
            continue

        # method call
        m = re.match(r"(\w+)\((\w+)\);", line)
        if m:
            ir.append(f"call {m.group(1)} {m.group(2)}")
            continue

        # assignment
        m = re.match(r"(\w+) = (\w+);", line)
        if m:
            ir.append(f"{m.group(1)} = {m.group(2)}")

    return "\n".join(ir)
