from os import path

def is_js(file):
    ext = path.splitext(file)[1]
    return ext.lower() in ['.js', '.jsx']

def get_relative_file_dir(file, startFile, no_extension=False, no_index=False):
    file_dir = path.dirname(file)
    if file_dir.startswith(startFile):
        res = "./" + path.relpath(file, startFile)
    else:
        res = path.relpath(file, startFile)

    if no_index and path.splitext(path.basename(file))[0] == 'index':
        return path.dirname(res)

    return path.splitext(res)[0] if no_extension else res

def guess_import_name(file):
    return path.splitext(path.basename(file))[0]