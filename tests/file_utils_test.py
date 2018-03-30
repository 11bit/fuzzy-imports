from nose.tools import eq_
from tools.file_utils import kebab_to_camel

def test_kebab_to_camel():
    eq_(kebab_to_camel('hello-world'), 'helloWorld')
    eq_(kebab_to_camel('helloWorld'), 'helloWorld')
    eq_(kebab_to_camel(''), '')
    eq_(kebab_to_camel('really_strange-named-file'), 'really_strangeNamedFile')
