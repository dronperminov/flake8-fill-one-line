import ast
from typing import Optional

from flake8_fill_one_line.utils import get_node_length, is_one_line


class IfExpAnalyzer:
    def get_length(self, node: ast.IfExp) -> Optional[int]:
        if is_one_line(node):
            return None  # skip one line expression

        # body if test else orelse
        length = node.col_offset
        length += get_node_length(node.body)
        length += 10 + get_node_length(node.test)
        length += get_node_length(node.orelse)
        return length
