import ast
import sys
from typing import Any, Generator, List, Tuple, Type

if sys.version_info < (3, 8):
    import importlib_metadata
else:
    import importlib.metadata as importlib_metadata


CALL_MSG = "FOL100 a function call can be written on one line"
ASSIGN_MSG = "FOL200 an assignment can be written on one line"


class Visitor(ast.NodeVisitor):
    def __init__(self, max_line_length: int = 160, skip_std_names: bool = True) -> None:
        self.max_line_length = max_line_length
        self.problems: List[Tuple[int, int, str]] = []
        self.skip_std_names = skip_std_names

    def __keyword_length(self, keyword: ast.keyword) -> int:
        if keyword.arg is None:  # kwarg
            raise NotImplementedError("kwargs not implemented")  # not now

        value_length = keyword.value.end_col_offset - keyword.value.col_offset
        return len(keyword.arg) + 1 + value_length  # arg=value

    def __check_call(self, node: ast.Call, lineno: int, col_offset: int, message: str) -> None:
        if node.lineno == node.end_lineno:
            return

        if self.skip_std_names and isinstance(node.func, ast.Name) and node.func.id in {"list", "dict", "tuple"}:
            return

        call_length = node.func.end_col_offset + 2  # name and two brackets
        args_lengths = []

        for i, arg in enumerate(node.args):
            if arg.lineno != arg.end_lineno:
                return

            args_lengths.append(arg.end_col_offset - arg.col_offset)

        for keyword in node.keywords:
            if keyword.value.lineno != keyword.value.end_lineno:
                return

            args_lengths.append(self.__keyword_length(keyword))

        call_length += sum(args_lengths) + (len(args_lengths) - 1) * 2

        if call_length <= self.max_line_length:
            self.problems.append((lineno, col_offset, f"{message} ({call_length} <= {self.max_line_length})"))

    def visit_Expr(self, node: ast.Expr) -> None:
        if isinstance(node.value, ast.Call):
            self.__check_call(node.value, node.lineno, node.col_offset, CALL_MSG)

        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> None:
        if isinstance(node.value, ast.Call):
            self.__check_call(node.value, node.lineno, node.col_offset, ASSIGN_MSG)

        self.generic_visit(node)


class Plugin:
    name = __name__
    version = importlib_metadata.version(__name__)

    def __init__(self, tree: ast.AST, max_line_length: int) -> None:
        self._tree = tree
        self.max_line_length = max_line_length

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        visitor = Visitor(max_line_length=self.max_line_length)
        visitor.visit(self._tree)

        for line, col, message in visitor.problems:
            yield line, col, message, type(self)
