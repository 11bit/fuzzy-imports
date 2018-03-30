def find_last_related_import(imports, path):
    for imp in reversed(imports):
        if imp.path == path:
            return imp.pos

    return imports[-1].pos if len(imports) > 0 else 0
