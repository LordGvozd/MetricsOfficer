from officer.metrics.loc import FileLengthChecker, FunctionLenghtChecker
from officer.config import Settings
from officer.models import MetricChecker


def get_all_metrics_checkers(settings: Settings) -> tuple[MetricChecker, ...]:
    return (
        FileLengthChecker(settings.max_file_len),
        FunctionLenghtChecker(settings.max_func_len),
    )
