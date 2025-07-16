"""Main script to run the Gemini AI chat client.

This script initializes the logging system and the Gemini chat client,
then starts an interactive chat session. It handles graceful exit
and logs any critical errors.
"""

from lib.gemini_tool import Client
from lib.log import Log


if __name__ == "__main__":
    # Initialize the logger for the main application.
    log = Log("gemini_log.csv")
    log.info("Starting Gemini Client...")

    try:
        # Initialize the Gemini chat client with a specific model.
        gemini = Client("gemini-2.0-flash")
        # Start the interactive chat session.
        gemini.start_chat()    
    except SystemExit:
        # Handle graceful exit of the chat application.
        log.info("Chat ended successfully.")  
    except:
        # Catch any other unexpected exceptions and log them as critical.
        log.critical()
