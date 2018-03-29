from nose.tools import eq_
from parameterized import parameterized

from tools.imports_parser import parse, Import

@parameterized([(
    'Basic imports',
    '''
import react from 'react';

import MyComponent from '../components';
import MyOtherComponent from '../components';
    ''',
    [
        Import('react', 1, 'react'),
        Import('MyComponent', 29, '../components'),
        Import('MyOtherComponent', 70, '../components'),
    ]
),
])

def test_exports(name, src, parsed_imports):
    eq_(parse(src), parsed_imports)
