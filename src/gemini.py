from google import genai
from pathlib import Path
from lib.log import Log
from collections import defaultdict
import json


class Client(genai.Client):
    def __init__(self, model: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.model = model

    @staticmethod
    def input_auth(method):
        def wrapper(self, *args, **kwargs):
            response = method(self, *args, **kwargs)
            if response:
                return response.text
            return "No response received."
        return wrapper

    @input_auth
    def respond(self, prompt: str):
        response = self.models.generate_content(
            model=self.model,
            contents=[prompt]
        )
        return response

def load_chat_history(file: Path):
    file.parent.mkdir(parents=True, exist_ok=True)
    if file.is_file():
        with file.open("r", encoding="utf-8") as f:
            content = f.read()
            if content:
                chat_history = defaultdict(dict, json.loads(content))
            else:
                chat_history = defaultdict(dict)
                chat_history["title"] = chat_title
                chat_history["history_index"] = 0
    else:
        chat_history = defaultdict(dict)
        chat_history["title"] = chat_title
        chat_history["history_index"] = 0
    return chat_history

def save_chat_history(file: Path, chat_history: dict) -> None:
    file.parent.mkdir(parents=True, exist_ok=True)
    with file.open("w", encoding="utf-8") as f:
        json.dump(chat_history, f, indent=4)
    return None

def update_chat_history(prompt="", response="", questions=1):
    if questions <= 1:
        questions = 2
    questions += 2

    chat_history["history_index"] += 1
    chat_history.update({
        chat_history["history_index"]: {
            "prompt": prompt,
            "response": response
        }
    })
        
    # Save chat history to file
    save_chat_history(chat_history_file, chat_history)

    # Check if the number of questions has reached the limit
    if len(chat_history) == (questions + previous_history_index):
        print(f"No more questions allowed. Exiting chat. | Max -> [{questions - 2}]")
        return "exit"
    return "continue"

def start_chat(model):
    # Welcome message
    print(
f"""Welcome to [{model.model}] Chat Client!
1. Check [response.csv] for [{model.model}]'s response.
2. Type 'exit' to end the chat.\n"""
    )

    # Initializes:
    # chat title, 
    # chat history, 
    # chat history file, and
    # history index
    global chat_title, chat_history, chat_history_file, previous_history_index

    # Enter chat title
    chat_title = input("Enter chat title: ")

    chat_history_file = Path(f"chat/history/{chat_title}.json")
    chat_history = load_chat_history(chat_history_file)
    previous_history_index = chat_history.get("history_index", 0)

    while True:
        prompt = input("Enter your prompt: ")
        print()
        response = model.respond(
f"""
chat history: {chat_history}
Instruction: 
    1. Always check the 'chat history' for context only.
    2. Return response for current prompt only.
    3. your knowledge base is the basis for your response.
    4. Do not repeat the chat history in your response.
prompt: {prompt}
"""
        )
        status = update_chat_history(prompt, response)

        file = Path(f"chat/response.csv")
        with file.open("w", encoding="utf-8") as f:
            f.write(response)
        
        if status == "exit" or prompt.lower() == "exit":
            print("Exiting chat...")
            print(f"Chat history saved to [{chat_history_file.name}]")
            exit()
      

if __name__ == "__main__":
    log = Log("gemini_log.csv")
    log.info("Starting Gemini Client...")
    try:
        gemini = Client(
            model="gemini-2.0-flash",
            api_key="AIzaSyBThzR-T3JpQERPgVVOaKeIGtanEILzgjA"
        )
        start_chat(gemini)    
    except SystemExit:
        log.info("Chat ended successfully.")  
    except:
        log.critical()
