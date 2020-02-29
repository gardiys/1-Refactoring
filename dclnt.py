import ast
import os
import collections

from nltk import pos_tag


def flat(_list):
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    return sum([list(item) for item in _list], [])


def is_verb(word):
    if not word:
        return False
    pos_info = pos_tag([word])
    return pos_info[0][1] == 'VB'


def get_trees(path, with_filenames=False, with_file_content=False):
    trees = []
    filenames = get_filenames(path)
    for filename in filenames:
        with open(filename, 'r', encoding='utf-8') as attempt_handler:
            main_file_content = attempt_handler.read()
        try:
            tree = ast.parse(main_file_content)
        except SyntaxError as e:
            print(e)
            tree = None
        if with_filenames:
            if with_file_content:
                trees.append((filename, main_file_content, tree))
            else:
                trees.append((filename, tree))
        else:
            trees.append(tree)
    print('trees generated')

    return [t for t in trees if t]


def get_filenames(path):
    filenames = []
    for dirname, dirs, files in os.walk(path, topdown=True):
        for file in files:
            if file.endswith('.py'):
                filenames.append(os.path.join(dirname, file))
                if len(filenames) == 100:
                    break
    print('total %s files' % len(filenames))
    return filenames


def get_all_names(tree):
    return [node.id for node in ast.walk(tree)
            if isinstance(node, ast.Name)]


def get_verbs_from_function_name(function_name):
    return [word for word in function_name.split('_') if is_verb(word)]


def get_all_words_in_path(path):
    trees = get_trees(path)
    function_names = get_all_functions(trees)

    words = []
    for name in function_names:
        words.append([n for n in name.split('_') if n])

    return flat(words)


def get_top_verbs_in_path(path):
    trees = get_trees(path)
    fncs = get_all_functions(trees)
    print('functions extracted')
    verbs = flat([get_verbs_from_function_name(function_name)
                  for function_name in fncs])
    return to_count(verbs)


def get_top_functions_names_in_path(path):
    trees = get_trees(path)
    nms = get_all_functions(trees)
    return to_count(nms)


def to_count(mass, top_size=10):
    return collections.Counter(mass).most_common(top_size)


def get_all_functions(trees):
    temp = []
    nms = []
    for tree in trees:
        nodes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                nodes.append(node.name.lower())
        temp.append(nodes)

    for f in flat(temp):
        if not (f.startswith('__') and f.endswith('__')):
            nms.append(f)
    return nms


if __name__ == "__main__":
    wds = []
    projects = [
        'django',
        'flask',
        'pyramid',
        'reddit',
        'requests',
        'sqlalchemy',
    ]
    for project in projects:
        path = os.path.join('.', project)
        wds += get_top_verbs_in_path(path)

    top_size = 200
    print('total %s words, %s unique' % (len(wds), len(set(wds))))
    for word, occurence in to_count(wds, top_size):
        print(word, occurence)
