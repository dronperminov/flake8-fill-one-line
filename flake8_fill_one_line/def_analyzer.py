import ast
from typing import Optional

from flake8_fill_one_line.utils import is_one_line


class DefAnalyzer:
    def get_length(self, node: ast.FunctionDef) -> Optional[int]:
        length = node.col_offset + len(f"def {node.name}():")
        args_lengths = []
        end_line = node.lineno

        for arg in node.args.args:
            if not is_one_line(arg):
                return None

            args_lengths.append(arg.end_col_offset - arg.col_offset)
            end_line = max(end_line, arg.end_lineno)

        if node.args.vararg is not None:
            if not is_one_line(node.args.vararg):
                return None

            args_lengths.append(node.args.vararg.end_col_offset - node.args.vararg.col_offset + 1)  # *vararg
            end_line = max(end_line, node.args.vararg.end_lineno)

        if node.args.kwarg is not None:
            if not is_one_line(node.args.kwarg):
                return None

            args_lengths.append(node.args.kwarg.end_col_offset - node.args.kwarg.col_offset + 2)  # **kvarg
            end_line = max(end_line, node.args.kwarg.end_lineno)

        length += sum(args_lengths) + (len(args_lengths) - 1) * 2

        for i, default in enumerate(node.args.defaults):
            offset = 1 if node.args.args[-(i + 1)].annotation is None else 3
            length += default.end_col_offset - default.col_offset + offset

        if node.returns is not None:
            length += node.returns.end_col_offset - node.returns.col_offset + 4  # " -> "
            end_line = max(end_line, node.returns.end_lineno)

        if end_line == node.lineno:
            return None

        return length
