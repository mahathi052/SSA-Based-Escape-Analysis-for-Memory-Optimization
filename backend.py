from ast_nodes import *
from ssa import SSAConverter
from escape_analysis import EscapeAnalyzer
from parser import parse_code

def analyze_program(code, mode):
    func = parse_code(code)

    ssa = SSAConverter()
    ssa_code = ssa.convert(func)

    analyzer = EscapeAnalyzer()
    allocation, heapified, reasons = analyzer.analyze(ssa_code, mode)

    return ssa_code, allocation, heapified, reasons

