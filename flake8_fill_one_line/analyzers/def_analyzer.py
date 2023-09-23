import ast
from typing import Optional

from flake8_fill_one_line.utils import get_node_length


class DefAnalyzer:
    def get_length(self, node: ast.FunctionDef) -> Optional[int]:
        length = node.col_offset + len(f"def {node.name}():")
        args_lengths = []
        end_line = node.lineno

        for arg in node.args.args:
            args_lengths.append(get_node_length(arg))
            end_line = max(end_line, arg.end_lineno)

        if node.args.vararg is not None:
            args_lengths.append(get_node_length(node.args.vararg) + 1)  # *vararg
            end_line = max(end_line, node.args.vararg.end_lineno)

        if node.args.kwarg is not None:
            args_lengths.append(get_node_length(node.args.kwarg) + 2)  # **kvarg
            end_line = max(end_line, node.args.kwarg.end_lineno)

        length += sum(args_lengths) + (len(args_lengths) - 1) * 2

        for i, default in enumerate(node.args.defaults):
            offset = 1 if node.args.args[-(i + 1)].annotation is None else 3
            length += default.end_col_offset - default.col_offset + offset

        if node.returns is not None:
            length += get_node_length(node.returns) + 4  # " -> "
            end_line = max(end_line, node.returns.end_lineno)

        if end_line == node.lineno:
            return None

        return length
