import unittest
import dclnt


class TestFileMethods(unittest.TestCase):

    def test_flat(self):
        actual = dclnt.flat([(1, 2), (3, 4)])
        expected = [1, 2, 3, 4]
        self.assertEqual(actual, expected)

    def test_is_verb(self):
        self.assertTrue(dclnt.is_verb("run"))
        self.assertFalse(dclnt.is_verb("wall"))

    def test_get_trees(self):
        path = r"./django/tests/model_forms"
        actual = [str(i) for i in dclnt.get_trees(path)]
        expected = ['<_ast.Module object at 0x0CB99B98>', '<_ast.Module object at 0x0CB99B08>',
                    '<_ast.Module object at 0x0CDC1688>', '<_ast.Module object at 0x0CCEC3A0>',
                    '<_ast.Module object at 0x0CBDDF88>']
        self.assertEqual(len(actual), len(expected))

    def test_get_filenames(self):
        path = r"./django/tests/model_forms"
        expected = ['./django/tests/model_forms\\models.py', './django/tests/model_forms\\tests.py',
                     './django/tests/model_forms\\test_modelchoicefield.py',
                     './django/tests/model_forms\\test_uuid.py', './django/tests/model_forms\\__init__.py']
        actual = dclnt.get_filenames(path)
        self.assertEqual(actual, expected)

    def test_get_all_words_in_path(self):
        path = r"./django/tests/admin_autodiscover"
        expected = ['test', 'double', 'call', 'autodiscover']
        actual = dclnt.get_all_words_in_path(path)
        self.assertEqual(expected, actual)

    def test_get_top_verbs_in_path(self):
        path = r"./django/tests/model_forms"
        expected = [('save', 11), ('replace', 3), ('run', 1)]
        actual = dclnt.get_top_verbs_in_path(path)
        self.assertEqual(expected, actual)

    def test_get_top_function_names_in_path(self):
        path = r"./django/tests/model_forms"
        expected = [('clean', 4), ('setuptestdata', 4), ('save', 2),
                    ('custom_upload_path', 2),
                    ('test_base_form', 2),
                    ('callback', 2), ('create_option', 2),
                    ('default_mode', 1),
                    ('default_category', 1),
                    ('today_callable_dict', 1)]
        actual = dclnt.get_top_functions_names_in_path(path)

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
