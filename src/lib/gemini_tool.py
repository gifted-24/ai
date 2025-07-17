"""gemini_tool.
This module provides a Client class for interacting with the Google Gemini API.

It handles chat session management, including loading and saving chat history,
sending prompts to the Gemini model, and processing responses.
"""

from google import genai
from collections import defaultdict
from pathlib import Path
import json


class Client(genai.Client):
    """Client
    A client for interacting with the Google Gemini API.

    This class extends google.genai.Client to provide additional functionalities
    for managing chat sessions, history, and user interaction.
    """
    def __init__(
        self, model: str,
        questions=100, context_window=15, *args, **kwargs
    ) -> None:
        """
        Initializes the Gemini Client.

        Args:
            model (str): The name of the Gemini model to use (e.g., "gemini-2.0-flash").
            questions (int, optional): The maximum number of questions allowed in a chat session. Defaults to 100.
            context_window (int, optional): The number of recent chat turns to include as context for the Gemini model. Defaults to 15.
            *args: Variable length argument list to pass to the base genai.Client constructor.
            **kwargs: Arbitrary keyword arguments to pass to the base genai.Client constructor.
        """
        super().__init__(*args, **kwargs)
        self.model = model
        self.questions = questions
        self.context_window = context_window

    @staticmethod
    def process_response(method):
        """
        A static method decorator to process the response from the Gemini API.

        This decorator extracts the text content from the API response.

        Args:
            method (callable): The method whose response needs to be processed.

        Returns:
            callable: A wrapper function that processes the method's response.
        """
        def wrapper(self, *args, **kwargs):
            response = method(self, *args, **kwargs)
            if response:
                return response.text
            return "No response received."
        return wrapper

    @process_response
    def respond(self, prompt: str) -> str:
        """
        Sends a prompt to the Gemini model and returns its response.

        Args:
            prompt (str): The user's input prompt.

        Returns:
            str: The text response from the Gemini model.
        """
        response = self.models.generate_content(
            model=self.model,
            contents=[prompt]
        )
        return response

    def load_history(self) -> dict:
        """
        Loads the chat history from a JSON file.

        If the history file does not exist or is empty, it initializes a new history.
        The history is stored in a defaultdict for flexible access.

        Returns:
            dict: The loaded or initialized chat history.
        """
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        if self.history_file.is_file() and self.history_file.stat().st_size > 0:
            with self.history_file.open("r", encoding="utf-8") as f:
                self.history = defaultdict(
                    dict, json.load(f)
                )
        else:
            self.history = defaultdict(dict)
            self.history["title"] = self.chat_title
            self.history["history_index"] = 0
        
        self.context = list(self.history.items())
        return self.history
    
    def save_history(self) -> None:
        """
        Saves the current chat history to a JSON file.
        """
        with self.history_file.open("w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=4)
        return None
    
    def update_history(self, prompt="", response="") -> str:
        """
        Updates the chat history with a new prompt and response.

        Also checks if the maximum number of questions for the session has been reached.

        Args:
            prompt (str, optional): The user's prompt. Defaults to "".
            response (str, optional): The Gemini model's response. Defaults to "".

        Returns:
            str: "continue" if the chat can continue, "exit" if the question limit is reached.
        """
        if self.questions < 1:
            self.questions = 1
    
        self.history["history_index"] += 1
        self.history.update({
            self.history["history_index"]: {
                "prompt": prompt,
                "response": response
            }
        })
        self.context.append(
            (self.history["history_index"], {
                "prompt": prompt,
                "response": response
            })
        )    
        # Save chat history to file
        self.save_history()
        
        # Check if the number of questions has reached the limit
        # (len(self.history) - 2) accounts for 'title' and 'history_index' keys
        if (len(self.history) - 2) == (self.questions + self.history_index):
            print(f"No more questions allowed. Exiting chat. | Max -> [{self.questions}]")
            return "exit"
        return "continue"
    
    def start_chat(self) -> str:
        """
        Starts an interactive chat session with the Gemini model.

        This method handles the main chat loop, taking user input,
        sending it to the Gemini model, displaying responses, and managing history.

        Returns:
            str: The name of the model used for the chat.
        """
        # Welcome message
        welcome_message = f"""
Welcome to [{self.model}] Chat Client!
    1. Check [response.csv] for [{self.model}]'s response.
    2. Type 'exit' to end the chat.\n"""
        print(welcome_message)
    
        # Enter chat title
        self.chat_title = input("Enter chat title: ")
        self.history_file = Path(f"chat/history/{self.chat_title}.json")
        self.history = self.load_history()
        self.history_index = self.history.get("history_index", 0)
    
        while True:
            text = input("\nEnter your prompt: ")
            prompt = f"""chat history: {self.context[-self.context_window:]}
Instruction: 
    1. Always check the 'chat history' for context only.
    2. Return response for current prompt only.
    3. your knowledge base is the basis for your response.  
    4. Do not repeat the chat history in your response.
    prompt: {text}"""
            response = self.respond(prompt)
            status = self.update_history(prompt, response)
    
            file = Path(f"chat/response.csv")
            with file.open("w", encoding="utf-8") as f:
                f.write(response)
                f.seek(0, 2)
            
            if status == "exit" or prompt.lower() == "exit":
                print("Exiting chat...")
                print(f"Chat history saved to [{self.history_file.name}]")
                exit()
        return self.model