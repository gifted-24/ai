"""
Unit tests for gemini.py main script using unittest and mock.

This test suite verifies the main application logic in gemini.py, which is the entry point for the Gemini AI chat client.

Testing Strategy:
- The main() function in gemini.py is designed to initialize logging, create the Gemini client, start the chat session, and handle errors gracefully.
- To enable effective unit testing, main() is refactored to accept injected dependencies (log and gemini), allowing us to pass MagicMock objects and assert behavior without running the actual chat loop or writing to disk.
- These tests ensure that logging and error handling work as intended for normal startup, unexpected exceptions, and graceful exits.

Test Cases:
1. test_main_success: Ensures normal startup logs the correct messages and starts the chat session.
2. test_main_critical_exception: Ensures unexpected exceptions are logged as critical errors.
3. test_main_system_exit: Ensures graceful exits (SystemExit) are logged appropriately.

Run these tests with unittest discovery or directly as a script.
"""

import unittest
from unittest.mock import MagicMock
import sys

class TestGeminiMain(unittest.TestCase):
    """
    Test suite for the main() function in gemini.py, covering startup, exception, and graceful exit scenarios.
    """
    def test_main_success(self):
        """
        Test that main() logs startup and starts the chat session successfully.
        - Verifies that 'Starting Gemini Client...' is logged.
        - Ensures gemini.start_chat() is called.
        """
        from src.gemini import main
        log = MagicMock()
        gemini = MagicMock()
        main(log=log, gemini=gemini)
        log.info.assert_any_call('Starting Gemini Client...')
        gemini.start_chat.assert_called()

    def test_main_critical_exception(self):
        """
        Test that main() logs a critical error if an unexpected exception occurs during chat startup.
        - Simulates an exception from gemini.start_chat().
        - Verifies that log.critical() is called to record the error.
        """
        from src.gemini import main
        log = MagicMock()
        gemini = MagicMock()
        gemini.start_chat.side_effect = Exception('Unexpected error')
        main(log=log, gemini=gemini)
        self.assertTrue(log.critical.called, "Expected log.critical to be called on exception.")

    def test_main_system_exit(self):
        """
        Test that main() logs a successful exit when SystemExit is raised during chat.
        - Simulates SystemExit from gemini.start_chat().
        - Verifies that 'Chat ended successfully.' is logged.
        """
        from src.gemini import main
        log = MagicMock()
        gemini = MagicMock()
        gemini.start_chat.side_effect = SystemExit()
        try:
            main(log=log, gemini=gemini)
        except SystemExit:
            pass  # Prevent the test runner from exiting
        self.assertTrue(
            any(call[0][0] == 'Chat ended successfully.' for call in log.info.call_args_list),
            "Expected log.info('Chat ended successfully.') to be called on SystemExit."
        )

if __name__ == "__main__":
    unittest.main()
