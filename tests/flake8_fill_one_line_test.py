import ast
import os
import unittest
from typing import Set

from flake8_fill_one_line import Plugin, CALL_MSG, ASSIGN_MSG


class Test(unittest.TestCase):
    def code_results(self, code: str, max_line_length: int = 160) -> Set[str]:
        tree = ast.parse(code)
        plugin = Plugin(tree, max_line_length)
        return {f'{line}:{col + 1} {msg}' for line, col, msg, _ in plugin.run()}

    def file_results(self, filename: str, max_line_length: int = 160) -> Set[str]:
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "test_files", filename))
        with open(path, "r", encoding="utf-8") as f:
            return self.code_results(f.read(), max_line_length=max_line_length)

    def test_no_breaks(self):
        self.assertEquals(self.code_results(""), set())
        self.assertEquals(self.code_results('f()'), set())
        self.assertEquals(self.code_results('f(1, 2, 3, 4)'), set())
        self.assertEquals(self.code_results('f(1, 2, a=3, foo_baz=4)'), set())
        self.assertEquals(self.file_results("simple_impossible.py"), set())

    def test_simple_possible(self):
        result = self.file_results("simple_possible.py")

        self.assertEquals(len(result), 4)
        self.assertIn(f'2:1 {CALL_MSG} (28 <= 160)', result)
        self.assertIn(f'7:1 {CALL_MSG} (84 <= 160)', result)
        self.assertIn(f'14:9 {CALL_MSG} (18 <= 160)', result)
        self.assertIn(f'19:1 {ASSIGN_MSG} (28 <= 160)', result)
