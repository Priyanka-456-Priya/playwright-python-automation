"""
Logging Utility
Configures logging for test execution with colored console output and file logging
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional
import colorlog


def setup_logger(
    name: str,
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    console_output: bool = True
) -> logging.Logger:
    """
    Setup logger with colored console output and optional file logging

    Args:
        name: Logger name
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file path
        console_output: Whether to output to console

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))

    # Remove existing handlers
    logger.handlers.clear()

    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    console_formatter = colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s%(reset)s',
        datefmt='%H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )

    # Console handler
    if console_output:
        # Use UTF-8 encoding for console to handle Unicode characters
        import io
        console_handler = logging.StreamHandler(
            io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        )
        console_handler.setLevel(getattr(logging, log_level.upper()))
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    # File handler
    if log_file:
        # Create log directory if it doesn't exist
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(getattr(logging, log_level.upper()))
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger


class TestLogger:
    """Logger specifically for test execution"""

    def __init__(self, log_dir: str = "reports"):
        """
        Initialize TestLogger

        Args:
            log_dir: Directory for log files
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Create timestamped log file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.log_dir / f"test_execution_{timestamp}.log"

        self.logger = setup_logger(
            name="TestExecution",
            log_level="INFO",
            log_file=str(self.log_file),
            console_output=True
        )

    def get_logger(self) -> logging.Logger:
        """Get logger instance"""
        return self.logger

    def log_test_start(self, test_name: str):
        """Log test start"""
        self.logger.info("=" * 80)
        self.logger.info(f"Starting Test: {test_name}")
        self.logger.info("=" * 80)

    def log_test_end(self, test_name: str, passed: bool, duration: float):
        """Log test end"""
        status = "PASSED" if passed else "FAILED"
        self.logger.info(f"Test {test_name} {status} in {duration:.2f}s")
        self.logger.info("=" * 80)

    def log_validation_result(self, endpoint: str, method: str, expected_code: int, actual_code: int, passed: bool):
        """Log validation result"""
        status = "[PASS]" if passed else "[FAIL]"
        if passed:
            self.logger.info(
                f"{status} {method} {endpoint} | Expected: {expected_code}, Got: {actual_code}"
            )
        else:
            self.logger.warning(
                f"{status} {method} {endpoint} | Expected: {expected_code}, Got: {actual_code}"
            )

    def log_error(self, message: str, exception: Optional[Exception] = None):
        """Log error"""
        self.logger.error(message)
        if exception:
            self.logger.exception(exception)

    def log_summary(self, total: int, passed: int, failed: int):
        """Log test summary"""
        self.logger.info("")
        self.logger.info("=" * 80)
        self.logger.info("TEST EXECUTION SUMMARY")
        self.logger.info("=" * 80)
        self.logger.info(f"Total Tests: {total}")
        self.logger.info(f"Passed: {passed} ({passed/total*100 if total > 0 else 0:.1f}%)")
        self.logger.info(f"Failed: {failed} ({failed/total*100 if total > 0 else 0:.1f}%)")
        self.logger.info("=" * 80)


if __name__ == "__main__":
    # Example usage
    test_logger = TestLogger()
    logger = test_logger.get_logger()

    test_logger.log_test_start("Test API Error Codes")
    logger.info("This is an info message")
    logger.warning("This is a warning")
    logger.error("This is an error")

    test_logger.log_validation_result(
        endpoint="/api/users",
        method="GET",
        expected_code=404,
        actual_code=404,
        passed=True
    )

    test_logger.log_test_end("Test API Error Codes", passed=True, duration=2.5)
    test_logger.log_summary(total=10, passed=8, failed=2)
