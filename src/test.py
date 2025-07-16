"""Unit tests for the Log class.

This script contains a test function to verify the functionality of the
Log class, including info, error, and critical logging levels.
"""

from lib.log import Log

def test_log():
    """Tests the logging capabilities of the Log class.

    This function creates a Log instance and tests its info, error, and
    critical logging methods by simulating different scenarios.
    """
    log = Log("test_log.csv")
    
    # Test info logging
    log.info("This is an info message.")
    
    # Test error logging by simulating a ZeroDivisionError
    try:
        division = 1 / 0  
    except ZeroDivisionError:
        log.error()
    
    # Test critical logging by simulating a ValueError
    try:
        raise ValueError("This is a critical error.")
    except ValueError:
        log.critical()

if __name__ == "__main__":
    test_log()
    print("Log tests completed successfully.")
