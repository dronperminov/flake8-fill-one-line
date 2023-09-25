import ast
from typing import Optional

from flake8_fill_one_line.utils import get_node_length, is_one_line


class CallAnalyzer:
    def __init__(self, skip_std_names: bool, skip_multiline_arguments: bool) -> None:
        self.skip_std_names = skip_std_names
        self.skip_multiline_arguments = skip_multiline_arguments

    def get_length(self, node: ast.Call) -> Optional[int]:
        if is_one_line(node):
            return None  # skip one line call

        if self.skip_std_names and isinstance(node.func, ast.Name) and node.func.id in {"list", "dict", "set", "tuple"}:
            return None

        args_lengths = []

        for arg in node.args:
            if self.skip_multiline_arguments and not is_one_line(arg):
                return None

            args_lengths.append(get_node_length(arg))

        for keyword in node.keywords:
            if self.skip_multiline_arguments and is_one_line(keyword) is False:
                return None

            args_lengths.append(get_node_length(keyword))

        length = node.func.col_offset + get_node_length(node.func) + 2
        length += sum(args_lengths) + (len(args_lengths) - 1) * 2
        return length
