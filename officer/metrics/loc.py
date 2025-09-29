import ast
from officer.types import (
    AstMetricChecker,
    MetricViolation,
    MetricsError,
)


class TooLargeFileViolation(MetricViolation):
    """You should write less code in one file."""


class TooLargeFunctionViolation(MetricViolation):
    """You should write less of code in one function."""


class FileLengthChecker:
    def __init__(self, max_file_len: int) -> None:
        self._max_file_len = max_file_len

    def find_violations(self, source: str) -> list[TooLargeFileViolation] | None:
        if source.count("\n") > self._max_file_len:
            return [TooLargeFileViolation()]
        return None


class FunctionLenghtChecker(AstMetricChecker):
    def __init__(self, max_func_len: int) -> None:
        super().__init__()

        self._max_func_len = max_func_len

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        function_code = ast.get_source_segment(self._source, node)

        if function_code is None:
            raise MetricsError("Cant get source code!")

        if function_code.count("\n") > self._max_func_len:
            self.add_violation(TooLargeFunctionViolation())

        self.generic_visit(node)
