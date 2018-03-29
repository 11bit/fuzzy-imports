def find_last_related_import(imports, path):
    for imp in reversed(imports):
        if imp.path == path:
            return imp.pos

    return 0