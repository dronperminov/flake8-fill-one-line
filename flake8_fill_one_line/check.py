import ast
from argparse import Namespace
from typing import Any, Generator, List, Tuple, Type, Union

from flake8.options.manager import OptionManager

from flake8_fill_one_line import __version__
from flake8_fill_one_line.analyzers.call_analyzer import CallAnalyzer
from flake8_fill_one_line.analyzers.def_analyzer import DefAnalyzer
from flake8_fill_one_line.analyzers.if_analyzer import IfAnalyzer
from flake8_fill_one_line.analyzers.if_exp_analyzer import IfExpAnalyzer
from flake8_fill_one_line.analyzers.import_analyzer import ImportAnalyzer
from flake8_fill_one_line.analyzers.with_analyzer import WithAnalyzer
from flake8_fill_one_line.utils import is_one_line

IMPORT_MSG = "FOL001 Import statement can be written in one line"
CALL_MSG = "FOL002 Function call can be written in one line"
ASSIGN_MSG = "FOL003 Assignment can be written in one line"
RETURN_MSG = "FOL004 Return statement can be written in one line"
DEF_MSG = "FOL005 Function definition can be written in one line"
WITH_MSG = "FOL006 With statement can be written in one line"
IF_MSG = "FOL007 If statement can be written in one line"


class Visitor(ast.NodeVisitor):
    def __init__(self, max_line_length: int = 160, skip_std_names: bool = True, skip_multiline_arguments: bool = True) -> None:
        self.max_line_length = max_line_length
        self.skip_std_names = skip_std_names
        self.skip_multiline_arguments = skip_multiline_arguments
        self.problems: List[Tuple[int, int, str]] = []

    def visit_Import(self, node: ast.Import) -> None:
        self.__check_import(node)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        self.__check_import_from(node)
        self.generic_visit(node)

    def visit_Expr(self, node: ast.Expr) -> None:
        self.__visit_expression(node, CALL_MSG)

    def visit_Assign(self, node: ast.Assign) -> None:
        self.__visit_expression(node, ASSIGN_MSG)

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        self.__visit_expression(node, ASSIGN_MSG)

    def visit_Return(self, node: ast.Return) -> None:
        self.__visit_expression(node, RETURN_MSG)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.__check_def(node)
        self.generic_visit(node)

    def visit_With(self, node: ast.With) -> None:
        self.__check_with(node)
        self.generic_visit(node)

    def visit_If(self, node: ast.If) -> None:
        self.__check_if(node)
        self.generic_visit(node)

    def __visit_expression(self, node: Union[ast.Expr, ast.Assign, ast.AugAssign, ast.Return], message: str) -> None:
        if isinstance(node.value, ast.Call):
            self.__check_call(node.value, node.lineno, node.col_offset, message)
        elif isinstance(node.value, ast.IfExp):
            self.__check_if_exp(node.value, node.lineno, node.col_offset, message)

        self.generic_visit(node)

    def __check_import(self, node: ast.Import) -> None:
        if is_one_line(node):
            return

        import_analyzer = ImportAnalyzer()
        length = import_analyzer.get_import_length(node)

        if length <= self.max_line_length:
            self.problems.append((node.lineno, node.col_offset, f"{IMPORT_MSG} ({length} <= {self.max_line_length})"))

    def __check_import_from(self, node: ast.ImportFrom) -> None:
        if is_one_line(node):
            return

        import_analyzer = ImportAnalyzer()
        length = import_analyzer.get_import_from_length(node)

        if length <= self.max_line_length:
            self.problems.append((node.lineno, node.col_offset, f"{IMPORT_MSG} ({length} <= {self.max_line_length})"))

    def __check_call(self, node: ast.Call, lineno: int, col_offset: int, message: str) -> None:
        call_analyzer = CallAnalyzer(skip_std_names=self.skip_std_names, skip_multiline_arguments=self.skip_multiline_arguments)
        length = call_analyzer.get_length(node)
        if length is not None and length <= self.max_line_length:
            self.problems.append((lineno, col_offset, f"{message} ({length} <= {self.max_line_length})"))

    def __check_if_exp(self, node: ast.IfExp, lineno: int, col_offset: int, message: str) -> None:
        if_exp_analyzer = IfExpAnalyzer()
        length = if_exp_analyzer.get_length(node)
        if length is not None and length <= self.max_line_length:
            self.problems.append((lineno, col_offset, f"{message} ({length} <= {self.max_line_length})"))

    def __check_def(self, node: ast.FunctionDef) -> None:
        def_analyzer = DefAnalyzer()
        length = def_analyzer.get_length(node)

        if length is not None and length <= self.max_line_length:
            self.problems.append((node.lineno, node.col_offset, f"{DEF_MSG} ({length} <= {self.max_line_length})"))

    def __check_with(self, node: ast.With) -> None:
        with_analyzer = WithAnalyzer()
        length = with_analyzer.get_length(node)

        if length is not None and length <= self.max_line_length:
            self.problems.append((node.lineno, node.col_offset, f"{WITH_MSG} ({length} <= {self.max_line_length})"))

    def __check_if(self, node: ast.If) -> None:
        if_analyzer = IfAnalyzer()
        length = if_analyzer.get_length(node)

        if length is not None and length <= self.max_line_length:
            self.problems.append((node.lineno, node.col_offset, f"{IF_MSG}"))


class FillOneLineChecker:
    name = "flake8-fill-one-line"
    version = __version__

    max_line_length = 160
    skip_std_names = True
    skip_multiline_arguments = True

    def __init__(self, tree: ast.AST) -> None:
        self._tree = tree

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        visitor = Visitor(max_line_length=self.max_line_length, skip_std_names=self.skip_std_names, skip_multiline_arguments=self.skip_multiline_arguments)
        visitor.visit(self._tree)

        for line, col, message in visitor.problems:
            yield line, col, message, type(self)

    @classmethod
    def add_options(cls, option_manager: OptionManager) -> None:
        option_manager.add_option("--skip-std-names", action="store_true", default=True, parse_from_config=True)
        option_manager.add_option("--skip-multiline-arguments", action="store_true", default=True, parse_from_config=True)

    @classmethod
    def parse_options(cls, options: Namespace) -> None:
        cls.max_line_length = options.max_line_length
        cls.skip_std_names = options.skip_std_names
        cls.skip_multiline_arguments = options.skip_multiline_arguments
