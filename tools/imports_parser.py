import re

class Import:
    def __init__(self, name, pos, path):
        self.name = name
        self.pos = pos
        self.path = path

    def __eq__(self, other):
        return vars(self) == vars(other)

    def __repr__(self):
        return str(vars(self))

    def is_node_modules(self):
        return path[0].isalnum()


regExp = re.compile('import (.*?) from "(.*?)"', re.MULTILINE | re.DOTALL)

def parse(src):
    src = src.replace('\'', '"')
    res = []

    for i in re.finditer(regExp, src):
        name, path = i.groups()
        res.append(Import(
            name=name,
            pos=i.start(),
            path=path
        ))

    return res
