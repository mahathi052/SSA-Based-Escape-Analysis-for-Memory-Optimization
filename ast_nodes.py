class Statement:
    pass

class NewObject(Statement):
    def __init__(self, var):
        self.var = var

class Assign(Statement):
    def __init__(self, target, source):
        self.target = target
        self.source = source

class Return(Statement):
    def __init__(self, var):
        self.var = var

class Function:
    def __init__(self, name, body):
        self.name = name
        self.body = body
class GlobalAssign(Statement):
    def __init__(self, name, var):
        self.name = name
        self.var = var
class Call(Statement):
    def __init__(self, func, arg):
        self.func = func
        self.arg = arg

