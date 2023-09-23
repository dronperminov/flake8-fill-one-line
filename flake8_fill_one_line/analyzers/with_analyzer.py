import ast
from typing import Optional

from flake8_fill_one_line.utils import get_node_length


class WithAnalyzer:
    def get_length(self, node: ast.With) -> Optional[int]:
        end_line = node.lineno
        length = node.col_offset + 6
        length += (len(node.items) - 1) * 2

        for item in node.items:
            length += get_node_length(item.context_expr)

            if item.optional_vars is not None:
                length += 4 + get_node_length(item.optional_vars)
                end_line = max(end_line, item.optional_vars.end_lineno)

            end_line = max(end_line, item.context_expr.end_lineno)

        if node.lineno == end_line:
            return None  # skip one line with statement

        return length
