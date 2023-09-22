import ast


def is_one_line(node: ast.AST) -> bool:
    return node.lineno == node.end_lineno
