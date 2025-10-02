import ast
from officer.models import (
    AstMetricChecker,
    EntityMetricViolation,
    FileMetricViolation,
    MetricsError,
)
from officer.config import Settings


class TooLargeFileViolation(FileMetricViolation):
    """You should write less code in one file."""

    code: int = 101


class TooLargeFunctionViolation(EntityMetricViolation):
    """You should write less of code in one function."""

    code: int = 102

class TooLargeMethodViolation(EntityMetricViolation):
    """You should write less of code in class method. """

    code: int = 103


class TooLargeClassViolation(EntityMetricViolation):
    """You should write less of code in one class. """

    code: int = 104

class FileLengthChecker:
    def __init__(self, settings: Settings) -> None:
        self._max_file_len = settings.max_file_len

    def find_violations(
        self, filename: str, source: str
    ) -> list[TooLargeFileViolation] | None:
        if source.count("\n") > self._max_file_len:
            return [TooLargeFileViolation(filename=filename)]
        return None


class FunctionLenghtChecker(AstMetricChecker):
    def __init__(self, settings: Settings) -> None:
        super().__init__()

        self._max_func_len = settings.max_func_len

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        function_code = ast.get_source_segment(self._source, node)

        if function_code is None:
            raise MetricsError("Cant get source code!")

        if function_code.count("\n") > self._max_func_len:
            self.add_violation(
                TooLargeFunctionViolation(
                    filename=self._filename, line=node.lineno, col=node.col_offset
                )
            )

        self.generic_visit(node)

class MethodLenghtChecker(AstMetricChecker):
    def __init__(self, settings: Settings) -> None:
        super().__init__()

        self._max_method_len = settings.max_method_len

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.FunctionDef):
                self._check_method_len(child)
        self.generic_visit(node)
                
    def _check_method_len(self, node: ast.FunctionDef) -> None:
        function_code = ast.get_source_segment(self._source, node)
        print(function_code)

        if function_code is None:
            raise MetricsError("Cant get source code!")

        if function_code.count("\n") > self._max_method_len:
            self.add_violation(
                TooLargeMethodViolation(
                    filename=self._filename, line=node.lineno, col=node.col_offset
                )
            )


class ClassLenghtChecker(AstMetricChecker):
    def __init__(self, settings: Settings) -> None:
        super().__init__()

        self._max_method_len = settings.max_method_len
    

    def _check_method_len(self, node: ast.FunctionDef) -> None:
        function_code = ast.get_source_segment(self._source, node)
        print(function_code)

        if function_code is None:
            raise MetricsError("Cant get source code!")

        if function_code.count("\n") > self._max_method_len:
            self.add_violation(
                TooLargeMethodViolation(
                    filename=self._filename, line=node.lineno, col=node.col_offset
                )
            )



