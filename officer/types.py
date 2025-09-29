from abc import ABC, abstractmethod
import ast
from typing import Protocol, runtime_checkable


class MetricViolation(ABC):
    """Base violation."""

    code: int


@runtime_checkable
class MetricChecker[Violation: MetricViolation](Protocol):
    def find_violations(self, source: str) -> list[Violation] | None: ...


class AstMetricChecker[Violation: MetricViolation](ABC, ast.NodeVisitor):
    def __init__(self) -> None:
        self._violations: list[Violation] = []
        self._source: str

    def add_violation(self, violation: Violation) -> None:
        self._violations.append(violation)

    def find_violations(self, source: str) -> list[Violation] | None:
        self._source = source
        tree = ast.parse(source)
        self.visit(tree)

        violations = self._violations if len(self._violations) > 0 else None

        return violations


class MetricsError(Exception): ...
