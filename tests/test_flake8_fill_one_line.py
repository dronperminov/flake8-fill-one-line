import ast
import os
import unittest
from typing import Set

from flake8_fill_one_line.check import FillOneLineChecker, CALL_MSG, ASSIGN_MSG, DEF_MSG, IMPORT_MSG


class TestFillOneLine(unittest.TestCase):
    def code_results(self, code: str, max_line_length: int = 160) -> Set[str]:
        tree = ast.parse(code)
        plugin = FillOneLineChecker(tree, max_line_length)
        return {f'{line}:{col + 1} {msg}' for line, col, msg, _ in plugin.run()}

    def file_results(self, filename: str, max_line_length: int = 160) -> Set[str]:
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "test_files", filename))
        with open(path, "r", encoding="utf-8") as f:
            return self.code_results(f.read(), max_line_length=max_line_length)

    def test_no_breaks(self):
        self.assertEqual(self.code_results(""), set())
        self.assertEqual(self.code_results('f()'), set())
        self.assertEqual(self.code_results('f(1, 2, 3, 4)'), set())
        self.assertEqual(self.code_results('f(1, 2, a=3, foo_baz=4)'), set())
        self.assertEqual(self.code_results('a = f(1, 2, 3)'), set())
        self.assertEqual(self.code_results('def f(a, b): pass'), set())
        self.assertEqual(self.code_results('def f(a, b):\n    pass'), set())

    def test_calls(self):
        result = self.file_results("calls.py")

        self.assertEqual(len(result), 5)
        self.assertIn(f'2:1 {CALL_MSG} (28 <= 160)', result)
        self.assertIn(f'7:1 {CALL_MSG} (84 <= 160)', result)
        self.assertIn(f'14:9 {CALL_MSG} (18 <= 160)', result)
        self.assertIn(f'19:1 {ASSIGN_MSG} (28 <= 160)', result)
        self.assertIn(f'32:1 {ASSIGN_MSG} (45 <= 160)', result)

    def test_definitions(self):
        result = self.file_results("definitions.py")

        self.assertEqual(len(result), 7)
        self.assertIn(f'4:1 {DEF_MSG} (15 <= 160)', result)
        self.assertIn(f'10:1 {DEF_MSG} (42 <= 160)', result)
        self.assertIn(f'17:1 {DEF_MSG} (81 <= 160)', result)
        self.assertIn(f'22:1 {DEF_MSG} (113 <= 160)', result)
        self.assertIn(f'28:1 {DEF_MSG} (42 <= 160)', result)
        self.assertIn(f'35:5 {DEF_MSG} (47 <= 160)', result)
        self.assertIn(f'41:5 {DEF_MSG} (49 <= 160)', result)

    def test_imports(self):
        result = self.file_results("imports.py")

        self.assertEquals(len(result), 4)
        self.assertIn(f'2:1 {IMPORT_MSG} (20 <= 160)', result)
        self.assertIn(f'4:1 {IMPORT_MSG} (16 <= 160)', result)
        self.assertIn(f'6:1 {IMPORT_MSG} (71 <= 160)', result)
        self.assertIn(f'12:5 {IMPORT_MSG} (30 <= 160)', result)
