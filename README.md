FuzzyImports
============

SublimeText 3 plugin to browse file system from quick panel and add a javascript module imports. Greatly influenced by FuzzyFileNav.

How to Use
----------

!["How to Use"](docs/FuzzyImports.gif?raw=True "How to Use")

1. Open JS file where you want to add an import.
2. Press Cmd + Alt + i combindation
3. In the opened quick panel navigate to the file you want to add and press Enter.
4. If it is js file and it has named exports it will show them in quick panel
5. Otherwise it will add a file as a default import

Features
--------

* Browse files from quick panel starting from target file's directory
* Quickly add javascript default exports
* View non-default exports and choose directly from quick panel
* Add non-js imports too

Credits
-------

* [FuzzyFileNav](https://github.com/facelessuser/FuzzyFileNav) - for idea and mechanics
* [Lark](https://github.com/erezsh/lark) - robust and easy to use parser for exports extraction
