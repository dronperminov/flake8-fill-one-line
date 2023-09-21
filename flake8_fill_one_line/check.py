import ast
from typing import Any, Generator, List, Tuple, Type, Union

from flake8_fill_one_line.utils import get_import_length, is_one_line, get_call_length, get_def_length, get_import_from_length

CALL_MSG = "FOL001 a function call can be written in one line"
ASSIGN_MSG = "FOL002 an assignment can be written in one line"
DEF_MSG = "FOL003 a function definition can be written in one line"
IMPORT_MSG = "FOL004 an import can be written in one line"


class Visitor(ast.NodeVisitor):
    def __init__(self, max_line_length: int = 160, skip_std_names: bool = True) -> None:
        self.max_line_length = max_line_length
        self.problems: List[Tuple[int, int, str]] = []
        self.skip_std_names = skip_std_names

    def visit_Expr(self, node: ast.Expr) -> None:
        self.__visit_expression(node, CALL_MSG)

    def visit_Assign(self, node: ast.Assign) -> None:
        self.__visit_expression(node, ASSIGN_MSG)

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        self.__visit_expression(node, ASSIGN_MSG)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.__check_def(node)
        self.generic_visit(node)

    def visit_Import(self, node: ast.ImportFrom) -> Any:
        self.__check_import(node)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        self.__check_import_from(node)
        self.generic_visit(node)

    def __visit_expression(self, node: Union[ast.Expr, ast.Assign, ast.AugAssign], message: str):
        if isinstance(node.value, ast.Call):
            self.__check_call(node.value, node.lineno, node.col_offset, message)

        self.generic_visit(node)

    def __check_call(self, node: ast.Call, lineno: int, col_offset: int, message: str) -> None:
        if is_one_line(node):
            return  # skip one line call

        if self.skip_std_names and isinstance(node.func, ast.Name) and node.func.id in {"list", "dict", "set", "tuple"}:
            return

        call_length = get_call_length(node)
        if call_length <= self.max_line_length:
            self.problems.append((lineno, col_offset, f"{message} ({call_length} <= {self.max_line_length})"))

    def __check_def(self, node: ast.FunctionDef) -> None:
        if node.lineno >= node.body[0].lineno - 1:
            return  # skip one line definition

        def_length = get_def_length(node)
        if def_length <= self.max_line_length:
            self.problems.append((node.lineno, node.col_offset, f"{DEF_MSG} ({def_length} <= {self.max_line_length})"))

    def __check_import_from(self, node: ast.ImportFrom) -> None:
        if is_one_line(node):
            return

        import_length = get_import_from_length(node)
        if import_length <= self.max_line_length:
            self.problems.append((node.lineno, node.col_offset, f"{IMPORT_MSG} ({import_length} <= {self.max_line_length})"))

    def __check_import(self, node: ast.Import) -> None:
        if is_one_line(node):
            return

        import_length = get_import_length(node)
        if import_length <= self.max_line_length:
            self.problems.append((node.lineno, node.col_offset, f"{IMPORT_MSG} ({import_length} <= {self.max_line_length})"))


class FillOneLineChecker:
    name = "flake8-fill-one-line"
    version = "0.1.0"

    def __init__(self, tree: ast.AST, max_line_length: int) -> None:
        self._tree = tree
        self.max_line_length = max_line_length

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        visitor = Visitor(max_line_length=self.max_line_length)
        visitor.visit(self._tree)

        for line, col, message in visitor.problems:
            yield line, col, message, type(self)
