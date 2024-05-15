import ast
import re
from typing import Union

import astunparse


def is_one_line(node: Union[ast.AST, ast.expr, ast.keyword]) -> bool:
    return node.lineno == node.end_lineno


def get_node_length(node: Union[ast.AST, ast.expr, ast.keyword]) -> int:
    if is_one_line(node):
        return node.end_col_offset - node.col_offset

    code = astunparse.unparse(node).strip()
    code = fix_tuple(code)
    return len(code)


def fix_tuple(code: str) -> str:
    matches = reversed([match for match in re.finditer(r"Tuple\[\(", code)])

    for match in matches:
        start, end = match.span()
        brace = 0
        bracket = 0

        for i, c in enumerate(code[end + 1:]):
            if c == "[":
                brace += 1
            elif c == "]":
                brace -= 1
            elif c == "(":
                bracket += 1
            elif c == ")":
                bracket -= 1

                if bracket < 0:
                    code = f"{code[:end - 1]}{code[end:end + i + 1]}{code[end + i + 2:]}"
                    break

    return code
