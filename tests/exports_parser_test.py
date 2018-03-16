from nose.tools import eq_
from parameterized import parameterized

from tools.exports_parser import parse_source

@parameterized([
(
    'Default Function Declaration 1',
    'export default function default_func_decl(){}',
    [{'name': 'export function', 'isDefault': True, 'value': 'default_func_decl'}]
),
(
    'Function Declaration 1',
    'export function default_func_decl(){}',
    [{'name': 'export function', 'isDefault': False, 'value': 'default_func_decl'}]
),
(
    'No whitespace Function Declaration 1',
    'exportdefault function default_func_decl(){}',
    []
),
(
    'No whitespace Function Declaration 2',
    'teexport function default_func_decl(){}',
    []
),
(
    'Default Function Declaration 2',
    '''
    import bla bla
    export default function default_func_decl(){
    export default function default_func_decl2(){

    }
    ''',
    [
        {'name': 'export function', 'isDefault': True, 'value': 'default_func_decl'},
        {'name': 'export function', 'isDefault': True, 'value': 'default_func_decl2'},
    ]
),
(
    'Anonymous Default Function Declaration',
    'export default function(){}',
    [
        {'name': 'export function', 'isDefault': True, 'value': 'Anonymous Function'},
    ]
),
(
    'Class Declaration',
    '''
    export
    default
    class MyComponent extends React
    ''',
    [
        {'name': 'export class', 'isDefault': True, 'value': 'MyComponent'},
    ]
),
(
    'export default expression',
    '''
    export default math.random()
    ''',
    [
        {'name': 'export default expression', 'isDefault': True, 'value': ''},
    ]
),
(
    'Simple const Declaration',
    'export const myVar=17;',
    [
        {'name': 'export const', 'isDefault': False, 'value': 'myVar'},
    ]
),
(
    'Simple nested Declaration',
    'export const {myVar}={myVar:17};',
    [
        {'name': 'export const', 'isDefault': False, 'value': 'myVar'},
    ]
),
(
    'Multiple nested Declaration',
    'export const { myVar, myOtherVar }={ myVar:17, myOtherVar: 22 };',
    [
        {'name': 'export const', 'isDefault': False, 'value': 'myVar'},
        {'name': 'export const', 'isDefault': False, 'value': 'myOtherVar'},
    ]
),
(
    'Multiple nested Declaration with Trailing comma',
    'export const { myVar, myOtherVar, }={ myVar:17, myOtherVar: 22 };',
    [
        {'name': 'export const', 'isDefault': False, 'value': 'myVar'},
        {'name': 'export const', 'isDefault': False, 'value': 'myOtherVar'},
    ]
),
(
    'Nested multilevel const Declaration',
    'export const { myVar, somOther: { nestedVar } } = { myVar: 3, somOther: { nestedVar: 5 } };',
    [
        {'name': 'export const', 'isDefault': False, 'value': 'myVar'},
        {'name': 'export const', 'isDefault': False, 'value': 'nestedVar'},
    ]
),
(
    'Renamed var',
    'export const { myVar: renamedVar } = { myVar: 3, somOther: { nestedVar: 5 } };',
    [
        {'name': 'export const', 'isDefault': False, 'value': 'renamedVar'},
    ]
),
(
    'Multiline var declaration',
    '''
export const {
    myVar: renamedVar,
    test,
    other,
    nested: { something, else },
} = { myVar: 3, somOther: { nestedVar: 5 } };
''',
    [
        {'name': 'export const', 'isDefault': False, 'value': 'renamedVar'},
        {'name': 'export const', 'isDefault': False, 'value': 'test'},
        {'name': 'export const', 'isDefault': False, 'value': 'other'},
        {'name': 'export const', 'isDefault': False, 'value': 'something'},
        {'name': 'export const', 'isDefault': False, 'value': 'else'},
    ]
),
(
    'export default variable',
    'export default MyComponent;',
    [
        {'name': 'export named variable', 'isDefault': True, 'value': 'MyComponent'},
    ]
),

#
# export const { shoulddest_4, shoulddest_5 } = 7
# export const { test: { internal } } = 7
# export default
# should4
#     export default should5
# test;export default should6
# exportdefault wrong1
# export defaultwrong2
# reexport default wrong3
# something else
])
def test_exports(name, src, parsed_exports):
    eq_(parse_source(src), parsed_exports)
