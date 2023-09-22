import ast
from typing import List, Optional


def is_one_line(node: ast.AST) -> bool:
    return node.lineno == node.end_lineno


def get_keyword_length(keyword: ast.keyword) -> Optional[int]:
    if not is_one_line(keyword.value):
        return None

    value_length = keyword.value.end_col_offset - keyword.value.col_offset

    if keyword.arg is None:
        return value_length + 2  # kwarg

    return len(keyword.arg) + 1 + value_length


def get_call_length(node: ast.Call) -> Optional[int]:
    length = node.func.end_col_offset + 2
    args_lengths = []

    for arg in node.args:
        if not is_one_line(arg):
            return None

        args_lengths.append(arg.end_col_offset - arg.col_offset)

    for keyword in node.keywords:
        keyword_length = get_keyword_length(keyword)

        if keyword_length is None:
            return None

        args_lengths.append(keyword_length)

    length += sum(args_lengths) + (len(args_lengths) - 1) * 2
    return length


def get_def_length(node: ast.FunctionDef) -> Optional[int]:
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


def get_import_names_length(names: List[ast.alias]) -> int:
    length = (len(names) - 1) * 2

    for name in names:
        length += len(name.name)

        if name.asname is not None:
            length += len(f" as {name.asname}")

    return length


def get_import_length(node: ast.Import) -> int:
    length = len("import ")
    length += get_import_names_length(node.names)
    return length


def get_import_from_length(node: ast.ImportFrom) -> int:
    length = node.col_offset + len(f"from {node.module} import ")
    length += get_import_names_length(node.names)
    return length
