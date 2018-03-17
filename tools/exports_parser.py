import re
import itertools

# import Imported.tools.lark
from lark import Lark, Transformer, Tree
from lark.lexer import Token

l = Lark('''

start: NEWLINE? (exports | other)+

exports: EXPORT DEFAULT? FUNCTION (_WS+ NAME)? "(" -> export_function
    | EXPORT DEFAULT? CLASS NAME -> export_class
    | EXPORT DEFAULT expression SEP? -> export_default_expression
    | EXPORT VAR var_decl "=" -> export_var

?var_decl: NAME -> var_name
         | obj_decl_group

obj_decl_group: "{" obj_decl ("," obj_decl)* ","? "}"
obj_decl: NAME -> var_name
    | obj_decl_pair
obj_decl_pair: NAME ":" obj_decl_pair_right
?obj_decl_pair_right: NAME -> var_name
    | obj_decl_group

expression : any+
//    | NAME SEP -> export_default_name

?any: /./
other: /./+ SEP?

EXPORT: SEP WS* "export" _WS+
DEFAULT: "default" _WS+
FUNCTION: "function"
CLASS.2: "class" _WS+
VAR: ("const" | "let" | "var") _WS+

_WS: WS | NEWLINE

SEP: (";" | NEWLINE)+

%import common.WS
%import common.CNAME -> NAME
%import common.LETTER
%import common.DIGIT


%import common.NEWLINE
%import common.WS_INLINE
%ignore WS

''', start='start', parser="lalr", lexer="contextual")

def flatten(names):
    return list(itertools.chain.from_iterable(names))

class CodeToExports(Transformer):
    def __init__(self):
        self.exports = []

    @staticmethod
    def isDefault(arr):
        return len([x for x in arr if x.type == 'DEFAULT']) == 1

    def start(self, _):
        return self.exports

    def export_default_function(self, s):
        names = [x for x in s if x.type == 'NAME']
        assert len(names) == 1, 'export_default_function parse error: should be only one NAME'

        self.exports.append(dict(
            name="export default function",
            value=names[0].value
        ))

    def export_default_name(self, s):
        names = [x for x in s if x.type == 'NAME']
        assert len(names) == 1, 'export_default_name parse error: should be only one NAME'

        self.exports.append(dict(
            name="export named variable",
            isDefault=True,
            value=names[0]
        ))

    def export_function(self, s):
        names = [x for x in s if x.type == 'NAME']
        assert len(names) <= 1, 'export_function parse error: should be no more than one NAME'

        func_name = names[0].value if len(names) == 1 else 'Anonymous Function'

        self.exports.append(dict(
            name="export function",
            isDefault=CodeToExports.isDefault(s),
            value=func_name
        ))

    def export_class(self, s):
        names = [x for x in s if x.type == 'NAME']
        assert len(names) == 1, 'export_function parse error: should be only one NAME'

        self.exports.append(dict(
            name="export class",
            isDefault=CodeToExports.isDefault(s),
            value=names[0].value
        ))

    def export_default_expression(self, s):
        expression_tree = [x for x in s if isinstance(x, Tree) and x.data == 'expression'][0]
        expression = ''.join(expression_tree.children)
        if re.match('^[^!@#%^&*()+-=<>/\\\\"\',.]*$', expression) is not None:
            name = expression
        else:
            name = ''

        self.exports.append(dict(
            name="export default expression" if name == '' else "export named variable",
            isDefault=True,
            value=name
        ))

    def export_var(self, s):
        names = [x for x in s if isinstance(x, list)]
        names = flatten(names)

        for name in names:
            self.exports.append(dict(
                name="export const",
                isDefault=False,
                value=name
            ))

    def obj_decl_group(self, s):
        print(s)
        names = []
        for token in s:
            if isinstance(token, Token):
                names.append(token)
            else:
                names += token
        return names

    def obj_decl(self, s):
        return flatten(s)

    def obj_decl_pair(self, s):
        return s[1]

    def var_name(self, s):
        return [s[0]]


def parse(file):
    with open(file) as f:
        return parse_source(f.read())


def parse_source(src):
    tree = l.parse(";" + src)

    print(tree.pretty())

    return CodeToExports().transform(tree)