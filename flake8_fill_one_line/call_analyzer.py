import ast
from typing import Optional

import astunparse

from .utils import is_one_line


class CallAnalyzer:
    def __init__(self, skip_std_names: bool) -> None:
        self.skip_std_names = skip_std_names

    def get_length(self, node: ast.Call) -> Optional[int]:
        if is_one_line(node):
            return None  # skip one line call

        if self.skip_std_names and isinstance(node.func, ast.Name) and node.func.id in {"list", "dict", "set", "tuple"}:
            return None

        if isinstance(node.func, ast.Name):
            return self.__get_simple_length(node)

        return node.col_offset + len(astunparse.unparse(node))  # this length may be invalid

    def __get_simple_length(self, node: ast.Call) -> Optional[int]:
        length = node.func.end_col_offset + 2
        args_lengths = []

        for arg in node.args:
            if not is_one_line(arg):
                return None

            args_lengths.append(arg.end_col_offset - arg.col_offset)

        for keyword in node.keywords:
            if not is_one_line(keyword.value):
                return None

            args_lengths.append(self.__get_keyword_length(keyword))

        length += sum(args_lengths) + (len(args_lengths) - 1) * 2
        return length

    def __get_keyword_length(self, keyword: ast.keyword) -> Optional[int]:
        value_length = keyword.value.end_col_offset - keyword.value.col_offset

        if keyword.arg is None:
            return value_length + 2  # kwarg

        return len(keyword.arg) + 1 + value_length
