import sublime
import sublime_plugin

import os
import os.path as path
from string import Template


import sys
import os
import sublime
import sublime_plugin

PPA_PATH = list()
PLUGIN_NAME = "Imported"

#-- Cannot use sublime.packages_path() with ST3 because of inconsistency
#-- of returned path between bootstap time vs running time.
#pkg_path = os.path.join(sublime.packages_path(), PLUGIN_NAME)
pkg_path = os.path.abspath(os.path.dirname(__file__))
libs_path = os.path.join(pkg_path, 'lib')
PPA_PATH.append(libs_path)

print('Included directory to sys.path :', PPA_PATH)
[sys.path.insert(0, p) for p in PPA_PATH if p not in sys.path]

try:
    from .tools.exports_parser import parse
    from .tools.file_utils import is_js, get_relative_file_dir, guess_import_name
    from .tools.imports_parser import parse as parse_imports
    from .tools.group_imports import find_last_related_import
except:
    sublime.error_message(
        '{0}: import error: {1}'.format(PLUGIN_NAME, sys.exc_info()[1]))
    raise


IMPORT_TEMPLATE = Template("import $name from '$path';")

PLATFORM = sublime.platform()


def debug_log(s):
    """Debug log."""
    # if sublime.load_settings(FUZZY_SETTINGS).get("debug", False):
    print("Imported: {}".format(s))

def get_root_path():
    """
    Get the root path.
    Windows doesn't have a root, so just
    return an empty string to represent its root.
    """

    return "" if PLATFORM == "windows" else "/"

def back_dir(cwd):
    """Step back a directory."""

    prev = path.dirname(cwd)

    return get_root_path() if prev == cwd else prev

class ImportedAddImportCommand(sublime_plugin.TextCommand):
    cwd = None
    startFile = None
    files = []
    exports = []

    def run(self, edit):
        name = self.view.file_name()
        directory = path.dirname(name)

        self.cwd = directory
        self.startFile = directory
        self.display_files(directory)

    def get_files(self, cwd):
        """Get files, folders, or window's drives."""

        # Get files/drives (windows).
        files = os.listdir(cwd)
        folders = []
        documents = []
        for f in files:
            valid = True
            full_path = path.join(cwd, f)

            # Store file/folder info.
            if valid:
                if not path.isdir(full_path):
                    documents.append(f)
                else:
                    folders.append(f + ("\\" if PLATFORM == "windows" else "/"))
        return [".."] + sorted(folders) + sorted(documents)

    def display_files(self, cwd, index=-1):
        """Display files in folder."""

        # Get the folders children
        # self.cls.status = True
        # status_cwd()
        self.files = self.get_files(cwd)

        # Make sure panel is down before loading a new one.
        # self.cls.view = None
        sublime.set_timeout(
            lambda: self.view.window().show_quick_panel(
                self.files, self.check_selection, 0, index, on_highlight=self.on_highlight
            ),
            0
        )

    def display_exports(self):
        exports = [x['name'] + ' ' + x['value'] for x in self.exports]
        sublime.set_timeout(
           lambda: self.view.window().show_quick_panel(
               exports, self.add_export, 0, -1, on_highlight=self.on_highlight
           ),
           0
        )

    def add_export(self, index):
        self.add_import_js_statement(self.cwd, self.exports[index])
        self.reset()

    def on_highlight(self, value):
        pass

    def check_selection(self, selection):
        """Check the users selection and navigate to directory or open file."""

        debug_log("Process selection")
        if selection > -1:
            # self.cls.fuzzy_reload = False
            # The first selection is the "go up a directory" option.
            directory = back_dir(self.cwd) if selection == 0 else path.join(self.cwd, self.files[selection])
            self.cwd = path.normpath(directory)

            # Check if the option is a folder or if we are at the root (needed for windows)
            # try:
            if (path.isdir(self.cwd) or self.cwd == get_root_path()):
                # List directories content
                self.display_files(self.cwd)
            else:
                # Import file
                if is_js(self.cwd):
                    try:
                        self.exports = parse(self.cwd)
                    except:
                        print(sys.exc_info())
                        self.exports = []

                    print('found', len(self.exports))

                    if len(self.exports) <= 1:
                        self.add_import_js_statement(self.cwd, self.exports)
                    else:
                        self.display_exports()
                else:
                    self.add_import_statement(self.cwd)
                    self.reset()

            # except Exception:
            #     # Inaccessible folder try backing up
            #     print(e)
            #     print("%s is not accessible!" % self.cwd)
            #     self.cwd = back_dir(self.cls.cwd)
            #     self.display_files(self.cwd)

    def add_import_statement(self, file):
        rel_path = get_relative_file_dir(file, self.startFile)
        fileName = guess_import_name(file)

        self.view.run_command('imported_insert_import', dict(name=fileName, path=rel_path))
        # print(IMPORT_TEMPLATE.substitute(name=fileName, path=rel_path))

    def add_import_js_statement(self, file, exports):
        if len(exports) == 1:
            meta = exports[0]
        else:
            # use defaults if we don't have an export name usually due to problems with parsing file
            meta = dict(isDefault=True, value=guess_import_name(file))

        rel_path = get_relative_file_dir(file, self.startFile, no_extension=True, no_index=True)

        import_name = meta['value'] if meta['value'] != '' else guess_import_name(file)
        export = import_name if meta['isDefault'] else '{ ' + import_name + ' }'

        self.view.run_command('imported_insert_import', dict(name=export, path=rel_path))
        # print(IMPORT_TEMPLATE.substitute(name=export, path=rel_path))

    def reset(self):
        self.cwd = None
        self.startFile = None
        self.files = []
        self.exports = []

    # def project(self):
    #     """Get folders from project."""

    #     data = self.window.project_data()
    #     if data is None:
    #         data = {}
    #     if "folders" not in data:
    #         data["folders"] = []

    #     if len(data["folders"]):
    #         self.window.run_command("fuzzy_project_folder_load")
    #     else:
    #         self.home()


class ImportedInsertImportCommand(sublime_plugin.TextCommand):
    def run(self, edit, name, path):
        text = IMPORT_TEMPLATE.substitute(name=name, path=path)
        file_content = self.view.substr(sublime.Region(0, self.view.size()))

        region = self.view.sel()[0]
        line = self.view.line(region)

        imports = parse_imports(file_content)
        last_import_line = self.view.line(imports[-1].pos)

        # if we are in the middle of the code than try to find suitable group for a new born import
        if line.begin() > last_import_line.begin():
            related_import_pos = find_last_related_import(imports, path)
            row, col = self.view.rowcol(related_import_pos)
            line = self.view.line(self.view.text_point(row + 1, col))

        self.insert_import(edit, line, text)

        self.view.sel().clear()
        self.view.sel().add(sublime.Region(line.begin() + 7, line.begin() + text.find(' from ')))


    def insert_import(self, edit, line, text):
        self.view.insert(edit, line.begin(), text + '\n')
