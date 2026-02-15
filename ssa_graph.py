from graphviz import Digraph

def build_ssa_graph(ssa_body, allocation, heapified):
    dot = Digraph(comment="SSA Graph", graph_attr={"rankdir": "LR"})

    for stmt in ssa_body:
        if stmt[0] == "new":
            _, var = stmt
            if var in heapified:
                color = "orange"
                label = f"{var}\nHeapified"
            elif allocation.get(var) == "STACK":
                color = "lightgreen"
                label = f"{var}\nSTACK"
            else:
                color = "lightcoral"
                label = f"{var}\nHEAP"

            dot.node(var, label, style="filled", fillcolor=color)

        elif stmt[0] == "assign":
            _, tgt, src = stmt
            dot.edge(src, tgt)

        elif stmt[0] == "call":
            _, src = stmt
            dot.node("CALL", "CALL", shape="box")
            dot.edge(src, "CALL")

        elif stmt[0] == "global":
            _, src = stmt
            dot.node("GLOBAL", "GLOBAL", shape="box")
            dot.edge(src, "GLOBAL")

        elif stmt[0] == "return":
            _, src = stmt
            dot.node("RETURN", "RETURN", shape="box")
            dot.edge(src, "RETURN")

    return dot
