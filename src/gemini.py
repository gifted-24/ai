"""Main script to run the Gemini AI chat client.

This script initializes the logging system and the Gemini chat client,
then starts an interactive chat session. It handles graceful exit
and logs any critical errors.
"""

from lib.gemini_tool import Client
from lib.log import Log


def main(log=None, gemini=None):
    # Allow dependency injection for testing
    if log is None:
        log = Log("gemini_log.csv")
    log.info("Starting Gemini Client...")

    try:
        if gemini is None:
            gemini = Client("gemini-2.0-flash")
        gemini.start_chat()
    except SystemExit:
        log.info("Chat ended successfully.")
    except:
        log.critical()

if __name__ == "__main__":
    main()
