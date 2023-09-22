import ast
import os
import unittest
from typing import Set

from flake8_fill_one_line.check import ASSIGN_MSG, CALL_MSG, DEF_MSG, FillOneLineChecker, IMPORT_MSG, RETURN_MSG


class TestFillOneLine(unittest.TestCase):
    def code_results(self, code: str) -> Set[str]:
        tree = ast.parse(code)
        plugin = FillOneLineChecker(tree)
        return {f"{line}:{col + 1} {msg}" for line, col, msg, _ in plugin.run()}

    def file_results(self, filename: str) -> Set[str]:
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "check_files", filename))
        with open(path, "r", encoding="utf-8") as f:
            return self.code_results(f.read())

    def test_no_breaks(self) -> None:
        self.assertEqual(self.code_results(""), set())
        self.assertEqual(self.code_results("import a, b, c, d"), set())
        self.assertEqual(self.code_results("from module import a, b, c, d"), set())
        self.assertEqual(self.code_results("f()"), set())
        self.assertEqual(self.code_results("f(1, 2, 3, 4)"), set())
        self.assertEqual(self.code_results("f(1, 2, a=3, foo_baz=4)"), set())
        self.assertEqual(self.code_results("a = f(1, 2, 3)"), set())
        self.assertEqual(self.code_results("def f(a, b): pass"), set())
        self.assertEqual(self.code_results("def f(a: int, b: int = 7) -> int:\n    pass"), set())

    def test_imports(self) -> None:
        result = self.file_results("imports.py")

        self.assertEqual(len(result), 4)
        self.assertIn(f"2:1 {IMPORT_MSG} (20 <= 160)", result)
        self.assertIn(f"4:1 {IMPORT_MSG} (16 <= 160)", result)
        self.assertIn(f"6:1 {IMPORT_MSG} (71 <= 160)", result)
        self.assertIn(f"17:5 {IMPORT_MSG} (30 <= 160)", result)

    def test_calls(self) -> None:
        result = self.file_results("calls.py")

        self.assertEqual(len(result), 8)
        self.assertIn(f"2:1 {CALL_MSG} (28 <= 160)", result)
        self.assertIn(f"7:1 {CALL_MSG} (84 <= 160)", result)
        self.assertIn(f"14:9 {CALL_MSG} (18 <= 160)", result)
        self.assertIn(f"19:1 {ASSIGN_MSG} (28 <= 160)", result)
        self.assertIn(f"32:1 {ASSIGN_MSG} (45 <= 160)", result)
        self.assertIn(f"43:1 {CALL_MSG} (61 <= 160)", result)
        self.assertIn(f"51:5 {RETURN_MSG} (26 <= 160)", result)
        self.assertIn(f"57:5 {DEF_MSG} (37 <= 160)", result)

    def test_definitions(self) -> None:
        result = self.file_results("definitions.py")

        self.assertEqual(len(result), 7)
        self.assertIn(f"4:1 {DEF_MSG} (15 <= 160)", result)
        self.assertIn(f"10:1 {DEF_MSG} (42 <= 160)", result)
        self.assertIn(f"17:1 {DEF_MSG} (81 <= 160)", result)
        self.assertIn(f"22:1 {DEF_MSG} (113 <= 160)", result)
        self.assertIn(f"28:1 {DEF_MSG} (42 <= 160)", result)
        self.assertIn(f"35:5 {DEF_MSG} (47 <= 160)", result)
        self.assertIn(f"41:5 {DEF_MSG} (49 <= 160)", result)
