import unittest

from FuzzyImports.tools.imports_parser import parse, Import

class TestImportsParser(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(parse('''
import react from 'react';

import MyComponent from '../components';
import MyOtherComponent from '../components';
    '''), [
        Import('react', 1, 'react'),
        Import('MyComponent', 29, '../components'),
        Import('MyOtherComponent', 70, '../components'),
    ], 'Basic imports')
