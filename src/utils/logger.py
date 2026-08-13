"""
Project : URL Shortener API

Project ID : 018

Runtime Logger and Execution Report
"""

from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter

from src.config import get_settings


class ExecutionLogger:
    """Manage runtime execution checkpoints and execution reports."""

    def __init__(
        self,
        report_file: Path | None = None,
    ) -> None:
        """Initialize the execution logger."""
        settings = get_settings()

        self._report_file = (
            report_file
            or settings.execution_report_file
        )

        self._start_time = perf_counter()
        self._start_timestamp = datetime.now(timezone.utc)
        self._checkpoints: list[str] = []
        self._status = "PASS"
        self._last_successful_checkpoint = "None"
        self._error_information = "None"

        self._ensure_log_directory()

    @property
    def report_file(self) -> Path:
        """Return the execution report path."""
        return self._report_file

    def start(self) -> None:
        """Record application execution start."""
        self._checkpoints.append("Application execution started.")

    def checkpoint(self, message: str) -> None:
        """Record a successful execution checkpoint."""
        self._checkpoints.append(message)
        self._last_successful_checkpoint = message

    def record_error(self, error: Exception) -> None:
        """Record an execution failure."""
        self._status = "FAIL"
        self._error_information = (
            f"{type(error).__name__}: {error}"
        )

        self._checkpoints.append(
            f"Execution error: {self._error_information}"
        )

    def write_report(self) -> Path:
        """Write the current execution report to disk."""
        duration = perf_counter() - self._start_time

        report_lines = [
            "URL Shortener API - Execution Report",
            "=" * 42,
            f"Project ID: 018",
            "Application Version: "
            f"{get_settings().app_version}",
            f"Execution Start (UTC): "
            f"{self._start_timestamp.isoformat()}",
            f"Execution End (UTC): "
            f"{datetime.now(timezone.utc).isoformat()}",
            f"Execution Duration (seconds): {duration:.3f}",
            f"Status: {self._status}",
            f"Last Successful Checkpoint: "
            f"{self._last_successful_checkpoint}",
            f"Error Information: {self._error_information}",
            "",
            "Execution Checkpoints",
            "-" * 42,
        ]

        report_lines.extend(
            f"{index}. {checkpoint}"
            for index, checkpoint in enumerate(
                self._checkpoints,
                start=1,
            )
        )

        self._report_file.write_text(
            "\n".join(report_lines) + "\n",
            encoding="utf-8",
        )

        return self._report_file

    def _ensure_log_directory(self) -> None:
        """Create the configured log directory when necessary."""
        self._report_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )


def create_execution_logger() -> ExecutionLogger:
    """Create and return a configured execution logger."""
    return ExecutionLogger()