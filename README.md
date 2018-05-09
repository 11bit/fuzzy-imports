FuzzyImports
============

FuzzyImports is a SublimeText 3 plugin that allows to browse file system via the quick panel and add javascript module imports. It is greatly influenced by [FuzzyFileNav](https://github.com/facelessuser/FuzzyFileNav).

How to Use
----------

!["How to Use"](docs/FuzzyImports.gif?raw=True "How to Use")

1. Open JS file where you want to add an import.
2. Press Cmd + Alt + i combindation to bing up the quick panel. It will show you a content of the opened file's directory.
3. Navigate to the file you want to add and press Enter.
4. If it is a js file and it has named exports it will show them in quick panel and give an ability to add it as a named import.
5. Otherwise it will add a file as a default import

Features
--------

* Browse files from quick panel starting from target file's directory
* Quickly add javascript default exports
* View non-default exports and choose directly from quick panel
* Add non-js imports too

Installation
------------

The easiest way to install FuzzyImports is via [Package Control](https://packagecontrol.io/).

1. Press ctrl + shift + p (Win, Linux) or cmd + shift + p (OSX) to bring up the quick panel and select "Package Control: Install Package". It will show a list of installable plugins
2. Select FuzzyImports and press Enter.
3. Restart Sublime to make sure everything is loaded properly

Credits
-------

* [FuzzyFileNav](https://github.com/facelessuser/FuzzyFileNav) - for idea and mechanics
* [Lark](https://github.com/erezsh/lark) - robust and easy to use parser for exports extraction
