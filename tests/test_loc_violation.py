from officer.metrics.loc import (
    FileLengthChecker,
    FunctionLenghtChecker,
    MethodLenghtChecker,
    ClassLenghtChecker,
    TooLargeFileViolation,
    TooLargeFunctionViolation,
    TooLargeMethodViolation,
    TooLargeClassViolation
)
from officer.config import Settings
from officer.models import MetricViolation

default_settins = Settings()
def _assert_violations(
    checker_output: list[MetricViolation] | None,
    expected_violations: list[type[MetricViolation]] | None,
):
    if checker_output is None:
        if expected_violations is None:
            return
        assert False

    assert len(checker_output) == len(expected_violations)
    for index in range(len(checker_output)):
        assert type(checker_output[index]) == expected_violations[index]


short_file = (
    """
print("Hello, world")
"""
    * 10
)

long_file = (
    """
print("I`m big!")
"""
    * 200
)

short_function_def = "def foo():\n" + "\tprint('Hello')\n" * 20
long_function_def = "def foo():\n" + "\tprint('Hello')\n" * 55


short_method_def = f"""
class Foo():
    def bar(self):
        {"print('Hello')\n" * 20}
"""

long_method_def = """
class Foo():
\tdef bar(self):\n""" + "\t\tprint(1)\n" * 40


def test_short_file():
    checker = FileLengthChecker(default_settins)

    _assert_violations(checker.find_violations("test", short_file), None)


def test_long_file():
    checker = FileLengthChecker(default_settins)

    _assert_violations(
        checker.find_violations("test", long_file), [TooLargeFileViolation]
    )


def test_short_function():
    checker = FunctionLenghtChecker(default_settins)

    _assert_violations(checker.find_violations("test", short_function_def), None)


def test_long_function():
    checker = FunctionLenghtChecker(default_settins)

    _assert_violations(
        checker.find_violations("test", long_function_def), [TooLargeFunctionViolation]
    )

def test_short_method():
    checker = MethodLenghtChecker(default_settins)

    _assert_violations(checker.find_violations("test", short_method_def), None)


def test_long_method():
    checker = MethodLenghtChecker(default_settins)

    _assert_violations(
        checker.find_violations("test", long_method_def), [TooLargeMethodViolation]
    )


