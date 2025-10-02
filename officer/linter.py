import os
from pathlib import Path
from typing import Sequence

from officer import config
from officer.models import (
    EntityMetricViolation,
    FileMetricViolation,
    MetricChecker,
    MetricViolation,
)
from officer.metrics.loc import FileLengthChecker, FunctionLenghtChecker


class Colors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    RESET = "\033[0m"


class Formater:
    def format(self, violation: MetricViolation) -> str:
        """Formats violation."""

        code = f"{Colors.RED}MO{violation.code}{Colors.RESET}"
        error_msg = violation.error_msg

        if isinstance(violation, FileMetricViolation):
            filename = violation.filename

            return f"{filename}: {code} {error_msg}"

        if isinstance(violation, EntityMetricViolation):
            filename = violation.filename
            line = violation.line
            col = violation.col

            return f"{filename}:{line}:{col}: {code} {error_msg}"

        return f"{code} {error_msg}"

    def print_violations(self, violations: Sequence[MetricViolation]) -> None:
        """Format and print sequence of violations."""

        for violation in violations:
            print(self.format(violation))


class Linter:
    def __init__(self, lint_path: Path, checkers: Sequence[MetricChecker]) -> None:
        self._lint_path = lint_path
        self._checkers = checkers
        self._formater = Formater()

        self._has_errors: bool = False

    def _lint_file(self, path: Path) -> None:
        if path.suffix != ".py":
            return
        all_violations = []
        for checker in self._checkers:
            violations = checker.find_violations(str(path), path.read_text())

            if violations:
                self._has_errors = True
                all_violations.extend(violations)
        self._formater.print_violations(all_violations)

    def _lint_dir(self, path: Path) -> None:
        for child in os.listdir(path):
            self._lint(path / child)

    def _lint(self, path: Path) -> None:
        if os.path.isfile(path):
            self._lint_file(path)
        else:
            self._lint_dir(path)

    def run(self):
        if os.path.exists(self._lint_path):
            self._lint(self._lint_path)
        else:
            print(Colors.RED + "File not found!" + Colors.RESET)

        if self._has_errors:
            exit(1)

        print(Colors.GREEN + "OK" + Colors.RESET)


if __name__ == "__main__":
    linter = Linter(
        Path("./officer"),
        checkers=(
            FileLengthChecker(config.MAX_FILE_LEN),
            FunctionLenghtChecker(config.MAX_FUNC_LEN),
        ),
    )
    linter.run()
