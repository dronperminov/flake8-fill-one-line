import ast
from typing import List


class ImportAnalyzer:
    def get_import_length(self, node: ast.Import) -> int:
        length = node.col_offset + len("import ")
        length += self.__get_import_names_length(node.names)
        return length

    def get_import_from_length(self, node: ast.ImportFrom) -> int:
        length = node.col_offset + len(f"from {node.module} import ")
        length += self.__get_import_names_length(node.names)
        return length

    def __get_import_names_length(self, names: List[ast.alias]) -> int:
        length = (len(names) - 1) * 2

        for name in names:
            length += len(name.name)

            if name.asname is not None:
                length += len(f" as {name.asname}")

        return length
