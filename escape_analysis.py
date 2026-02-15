class EscapeAnalyzer:
    def analyze(self, ssa_body, mode="conservative"):
        objects = {}
        allocation = {}
        heapified = set()
        reasons = {}

        # Step 1: optimistic stack allocation
        for stmt in ssa_body:
            if stmt[0] == "new":
                obj = stmt[1]
                objects[obj] = obj
                allocation[obj] = "STACK"

        # Strict mode: everything escapes
        if mode == "strict":
            for obj in allocation:
                allocation[obj] = "HEAP"
                heapified.add(obj)
                reasons[obj] = "Strict mode: assumed escaping"
            return allocation, heapified, reasons

        # Step 2: detect escape
        for stmt in ssa_body:
            if stmt[0] == "return":
                _, src = stmt
                if src in objects:
                    allocation[src] = "HEAP"
                    heapified.add(src)
                    reasons[src] = "Returned from method"

            elif stmt[0] == "call" and mode == "conservative":
                _, src = stmt
                if src in objects:
                    allocation[src] = "HEAP"
                    heapified.add(src)
                    reasons[src] = "Escapes via function call"

            elif stmt[0] == "global":
                _, src = stmt
                if src in objects:
                    allocation[src] = "HEAP"
                    heapified.add(src)
                    reasons[src] = "Stored in global variable"

            elif stmt[0] == "assign":
                _, tgt, src = stmt
                if src in objects:
                    objects[tgt] = objects[src]

        return allocation, heapified, reasons
