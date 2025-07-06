from pathlib import Path
import logging
import traceback
import sys

Path("log").mkdir(parents=True, exist_ok=True)  # Ensure log directory exists

class Log:
    def __init__(self, file_name: str='log.csv') -> None:
        logging.basicConfig(
            filename=Path(f"log/{file_name}"),
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            encoding='utf-8'
        )

    def _get_error_details(self):
        error_type, message, tracebk = sys.exc_info()
        error_name = error_type.__name__

        frames = traceback.extract_tb(tracebk)
        frame = next(
            (frame for frame in reversed(frames) if frame.filename == __file__), frames[-1]
        )
        file_name = Path(frame.filename).name
        line_no = frame.lineno

        error_details = {
            "ERROR": error_name,
            "Message": str(message),
            "File": file_name,
            "Line": line_no
        }
        return error_details

    def info(self, message: str) -> None:
        if message:
            logging.info(message)
        else:
            logging.info("No message provided.")
        return None
    
    def error(self, message: str=None) -> None:
        error_details = self._get_error_details()
        if message:
            error_details["message"] = message
        logging.error("%s", error_details)  
        return None
    
    def critical(self, message: str=None) -> None:
        error_details = self._get_error_details()
        if message:
            error_details["message"] = message
        logging.critical("%s", error_details)
        return None
    
