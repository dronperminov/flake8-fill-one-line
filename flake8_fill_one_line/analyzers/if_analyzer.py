import ast
from typing import Optional

from flake8_fill_one_line.utils import get_node_length, is_one_line


class IfAnalyzer:
    def get_length(self, node: ast.If) -> Optional[int]:
        if is_one_line(node.test):
            return None  # skip one line conditions

        length = node.col_offset + 4 + get_node_length(node.test)
        return length
