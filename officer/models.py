from abc import ABC, abstractmethod
import ast
import string
from typing import Protocol, runtime_checkable

from officer.config import Settings


class MetricViolation:
    """Base violation."""

    code: int
    error_msg: str



class FileMetricViolation(MetricViolation):
    """File metric violation."""

    def __init__(self, filename: str) -> None:
        self.filename = filename


class EntityMetricViolation(MetricViolation):
    """Code entity (function, class, etc) metric violation."""

    def __init__(self, filename: str, line: int, col: int) -> None:
        self.filename = filename
        self.line = line
        self.col = col


@runtime_checkable
class MetricChecker[Violation: MetricViolation](Protocol):
    def __init__(self, settings: Settings) -> None: ...
    def find_violations(self, filename: str, source: str) -> list[Violation] | None: ...


class AstMetricChecker[Violation: MetricViolation](ABC, ast.NodeVisitor):
    def __init__(self) -> None:
        self._violations: list[Violation] = []
        self._source: str

    def add_violation(self, violation: Violation) -> None:
        self._violations.append(violation)

    def find_violations(self, filename: str, source: str) -> list[Violation] | None:
        self._source = source
        self._filename = filename

        tree = ast.parse(source)
        self.visit(tree)

        violations = self._violations if len(self._violations) > 0 else None

        return violations


class MetricsError(Exception): ...
