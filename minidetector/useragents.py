import os.path


def load_from_search_strings_file():
    f = None
    try:
        f = open(os.path.join(os.path.dirname(__file__), 'search_strings.txt'))
        ss = f.readlines()
    finally:
        if f:
            f.close()
    return [s.strip() for s in ss if not s.startswith('#')]

search_strings = load_from_search_strings_file()
