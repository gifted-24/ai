from lib.gemini_tool import Client, start_chat
from lib.log import Log


if __name__ == "__main__":
    log = Log("gemini_log.csv")
    log.info("Starting Gemini Client...")
    try:
        gemini = Client("gemini-2.0-flash")
        start_chat(gemini)    
    except SystemExit:
        log.info("Chat ended successfully.")  
    except:
        log.critical()
