from lib.log import Log

def test_log():
    log = Log("test_log.csv")
    
    # Test info logging
    log.info("This is an info message.")
    
    # Test error logging
    try:
        1 / 0  # This will raise a ZeroDivisionError
    except ZeroDivisionError:
        log.error()
    
    # Test critical logging
    try:
        raise ValueError("This is a critical error.")
    except ValueError:
        log.critical()

if __name__ == "__main__":
    test_log()
    print("Log tests completed successfully.")