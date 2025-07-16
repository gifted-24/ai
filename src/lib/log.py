"""This module provides a custom logging utility for the AI project.

It defines a `Log` class that allows logging messages to a CSV file
with different severity levels (info, error, critical) and includes
detailed error information when exceptions occur.
"""

from pathlib import Path
import logging
import traceback
import sys

# Ensure the log directory exists
Path("log").mkdir(parents=True, exist_ok=True)

class Log:
    """A custom logging class that writes log messages to a CSV file.

    Logs include timestamp, level, message, error details (if applicable),
    file name, and line number.
    """
    def __init__(
        self, file_name: str='log.csv',
        header_row: str='DATE,LEVEL,MESSAGE,ERROR,FILE,LINE'
    ):
        """
        Initializes the Log instance.

        Args:
            file_name (str, optional): The name of the CSV file to log to. Defaults to 'log.csv'.
            header_row (str, optional): The header row for the CSV file. Defaults to 'DATE,LEVEL,MESSAGE,ERROR,FILE,LINE'.
        """
        self.log_file = Path(f"log/{file_name}")
        logging.basicConfig(
            filename=self.log_file,
            filemode='a',
            level=logging.INFO,
            format='%(asctime)s,%(levelname)s,%(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            encoding='utf-8'
        )
        self.fields = header_row.split(',')
        # Write header if the file is new or empty
        if not self.log_file.is_file() or self.log_file.stat().st_size == 0:
            with self.log_file.open('w') as f:
                f.write(f"{header_row}\n")
                f.seek(0, 2)
    
    def _get_error_details(self):
        """
        Extracts detailed information about the current exception.

        This method captures the error type, message, and the file/line number
        where the error occurred, prioritizing the location within this log module
        if applicable, otherwise falling back to the last frame.

        Returns:
            dict: A dictionary containing error details (error, message, file, line).
        """
        error_type, message, tracebk = sys.exc_info()
        error_name = error_type.__name__

        frames = traceback.extract_tb(tracebk)
        # Attempt to find the frame within this file, otherwise use the last frame
        frame = next(
            (frame for frame in reversed(frames) if frame.filename == __file__), frames[-1]
        )
        file_name = Path(frame.filename).name
        line_no = frame.lineno

        error_details = {
            "error": error_name,
            "message": str(message).replace(',', '.'), # Replace commas to avoid CSV formatting issues
            "file": file_name,
            "line": line_no
        }
        return error_details

    def info(self, message: str) -> None:
        """Logs an informational message.

        Args:
            message (str): The message to log.
        """
        if message:
            message = message.replace(',', '.') # Replace commas to avoid CSV formatting issues
            logging.info(message)
        else:
            logging.info('No message provided.')
        return None
    
    def error(self, message: str=None) -> None:
        """Logs an error message with detailed exception information.

        Args:
            message (str, optional): An optional custom message to include with the error. Defaults to None.
        """
        error_details = self._get_error_details()
        if message:
            error_details["message"] = message.replace(',', '.')
        logging.error(
            "%s,%s,%s,%s", 
            error_details['error'],
            error_details['message'],
            error_details['file'], 
            error_details['line']
        )
        return None
    
    def critical(self, message: str=None) -> None:
        """Logs a critical error message with detailed exception information.

        Args:
            message (str, optional): An optional custom message to include with the critical error. Defaults to None.
        """
        error_details = self._get_error_details()
        if message:
            error_details["message"] = message.replace(',', '.')
        logging.critical(
            "%s,%s,%s,%s", 
            error_details['error'],
            error_details['message'],
            error_details['file'], 
            error_details['line']
        )
        return None