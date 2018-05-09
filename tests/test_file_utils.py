import unittest

from FuzzyImports.tools.file_utils import kebab_to_camel

class TestFileUtils(unittest.TestCase):
    def test_kebab_to_camel(self):
        self.assertEqual(kebab_to_camel('hello-world'), 'helloWorld')
        self.assertEqual(kebab_to_camel('helloWorld'), 'helloWorld')
        self.assertEqual(kebab_to_camel(''), '')
        self.assertEqual(kebab_to_camel('really_strange-named-file'), 'really_strangeNamedFile')
