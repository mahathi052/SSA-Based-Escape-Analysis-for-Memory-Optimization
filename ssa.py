class SSAConverter:
    def __init__(self):
        self.version = {}

    def new_version(self, var):
        self.version[var] = self.version.get(var, 0) + 1
        return f"{var}{self.version[var]}"

    def convert(self, function):
        ssa_body = []
        var_map = {}

        for stmt in function.body:
            if stmt.__class__.__name__ == "NewObject":
                ssa_var = self.new_version(stmt.var)
                var_map[stmt.var] = ssa_var
                ssa_body.append(("new", ssa_var))

            elif stmt.__class__.__name__ == "Assign":
                src = var_map[stmt.source]
                tgt = self.new_version(stmt.target)
                var_map[stmt.target] = tgt
                ssa_body.append(("assign", tgt, src))

            elif stmt.__class__.__name__ == "Return":
                ssa_body.append(("return", var_map[stmt.var]))
            
            elif stmt.__class__.__name__ == "GlobalAssign":
                src = var_map[stmt.var]
                ssa_body.append(("global", src))
            elif stmt.__class__.__name__ == "Call":
                src = var_map[stmt.arg]
                ssa_body.append(("call", src))



        return ssa_body
