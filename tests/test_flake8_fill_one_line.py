import ast
import os
import sys
import unittest
from typing import Set

from flake8_fill_one_line.check import ASSIGN_MSG, CALL_MSG, DEF_MSG, FillOneLineChecker, IF_MSG, IMPORT_MSG, RETURN_MSG, WITH_MSG
from flake8_fill_one_line.utils import fix_tuple


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
        python_version = sys.version_info[0:2]

        self.assertEqual(len(result), 9 if python_version >= (3, 9) else 5)
        self.assertIn(f"2:1 {CALL_MSG} (28 <= 160)", result)
        self.assertIn(f"14:9 {CALL_MSG} (18 <= 160)", result)
        self.assertIn(f"51:5 {RETURN_MSG} (26 <= 160)", result)
        self.assertIn(f"57:5 {DEF_MSG} (37 <= 160)", result)
        self.assertIn(f"65:9 {RETURN_MSG} (64 <= 160)", result)

        if python_version >= (3, 9):
            self.assertIn(f"7:1 {CALL_MSG} (84 <= 160)", result)
            self.assertIn(f"19:1 {ASSIGN_MSG} (28 <= 160)", result)
            self.assertIn(f"32:1 {ASSIGN_MSG} (45 <= 160)", result)
            self.assertIn(f"43:1 {CALL_MSG} (61 <= 160)", result)

    def test_definitions(self) -> None:
        result = self.file_results("definitions.py")

        self.assertEqual(len(result), 11)
        self.assertIn(f"4:1 {DEF_MSG} (15 <= 160)", result)
        self.assertIn(f"10:1 {DEF_MSG} (42 <= 160)", result)
        self.assertIn(f"17:1 {DEF_MSG} (81 <= 160)", result)
        self.assertIn(f"22:1 {DEF_MSG} (113 <= 160)", result)
        self.assertIn(f"28:1 {DEF_MSG} (42 <= 160)", result)
        self.assertIn(f"35:5 {DEF_MSG} (47 <= 160)", result)
        self.assertIn(f"41:5 {DEF_MSG} (49 <= 160)", result)
        self.assertIn(f"56:5 {DEF_MSG} (132 <= 160)", result)
        self.assertIn(f"69:5 {DEF_MSG} (112 <= 160)", result)
        self.assertIn(f"77:5 {DEF_MSG} (152 <= 160)", result)
        self.assertIn(f"84:5 {DEF_MSG} (160 <= 160)", result)

    def test_with_statements(self) -> None:
        result = self.file_results("with_statements.py")

        self.assertEqual(len(result), 3)
        self.assertIn(f"7:1 {WITH_MSG} (32 <= 160)", result)
        self.assertIn(f"11:1 {WITH_MSG} (53 <= 160)", result)

    def test_if_statements(self) -> None:
        result = self.file_results("if_statements.py")

        self.assertEqual(len(result), 5)
        self.assertIn(f"22:1 {IF_MSG}", result)
        self.assertIn(f"29:1 {IF_MSG}", result)
        self.assertIn(f"35:5 {IF_MSG}", result)
        self.assertIn(f"38:5 {IF_MSG}", result)
        self.assertIn(f"44:5 {IF_MSG}", result)

    def test_utils(self) -> None:
        self.assertEqual(fix_tuple("Tuple[(int, int)]"), "Tuple[int, int]")
        self.assertEqual(fix_tuple("Tuple[(int, Tuple[int])]"), "Tuple[int, Tuple[int]]")
        self.assertEqual(fix_tuple("Tuple[(int, Tuple[(int, str, float)])]"), "Tuple[int, Tuple[int, str, float]]")
        self.assertEqual(fix_tuple("List[List[Tuple[(int, int, int)]]]"), "List[List[Tuple[int, int, int]]]")
        self.assertEqual(fix_tuple("Tuple[(Tuple[(int, int)], Tuple[(float, int, str)], int)]"), "Tuple[Tuple[int, int], Tuple[float, int, str], int]")
