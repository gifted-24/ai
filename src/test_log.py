"""Unit tests for the Log class using unittest framework.

This script contains test cases to verify the functionality of the
Log class, including info, error, and critical logging levels.
"""

import unittest
from pathlib import Path
from lib.log import Log

class TestLog(unittest.TestCase):
    LOG_FILE = "test_log.csv"

    def setUp(self):
        # Remove log file if it exists before each test
        import logging
        logging.shutdown()
        log_path = Path("log") / self.LOG_FILE
        if log_path.exists():
            log_path.unlink()
        self.log = Log(self.LOG_FILE)

    def tearDown(self):
        # Shutdown logging and clean up log file after each test
        import logging
        logging.shutdown()
        log_path = Path("log") / self.LOG_FILE
        if log_path.exists():
            log_path.unlink()

    def test_info_logging(self):
        self.log.info("This is an info message.")
        from pathlib import Path
        log_path = Path("log") / self.LOG_FILE
        with log_path.open("r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("INFO", content)
        self.assertIn("This is an info message.", content)

    def test_error_logging(self):
        try:
            _ = 1 / 0
        except ZeroDivisionError:
            self.log.error("ZeroDivisionError occurred")
        from pathlib import Path
        log_path = Path("log") / self.LOG_FILE
        with log_path.open("r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("ERROR", content)
        self.assertIn("ZeroDivisionError", content)
        self.assertIn("ZeroDivisionError occurred", content)

    def test_critical_logging(self):
        try:
            raise ValueError("This is a critical error.")
        except ValueError:
            self.log.critical("Critical error occurred")
        from pathlib import Path
        log_path = Path("log") / self.LOG_FILE
        with log_path.open("r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("CRITICAL", content)
        self.assertIn("ValueError", content)
        self.assertIn("Critical error occurred", content)

if __name__ == "__main__":
    unittest.main()
