# AI Project

## Overview
This project is focused on artificial intelligence and includes various functionalities implemented in Python. The main component of the project is encapsulated in the `gemini.py` file, which contains the core algorithms and classes related to AI.

## Project Structure

```text
ai/
├── src/
│   ├── lib/
│   │   ├── __init__.py
│   │   ├── gemini_tool.py
│   │   └── log.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── gemini_test.py
│   │   └── log_test.py
│   ├── __init__.py
│   └── gemini.py
├── run.py
├── test.py
├── requirements.txt
├── LICENSE
└── README.md
```

## Testing
The project includes a comprehensive test suite using Python's unittest framework. The tests cover:
- Gemini main functionality (startup, error handling, graceful exit)
- Logging system (critical, error, info levels)

To run the tests:
```bash
python -m unittest -v test
```

## Installation
To set up the project, you need to install the required dependencies. You can do this by running the following command in your terminal:

```bash
pip install -r requirements.txt
```

### Google API Key Setup

This project interacts with the Google Gemini API, which requires an API key for authentication. Follow these steps to obtain and configure your API key:

1.  **Obtain a Google API Key**:
    *   Go to the Google AI Studio website: [https://aistudio.google.com/](https://aistudio.google.com/)
    *   Sign in with your Google account.
    *   Create a new API key if you don't have one already.

2.  **Configure the API Key as an Environment Variable**:
    *   It is recommended to set your API key as an environment variable to keep it secure and out of your codebase.
    *   Open your shell's configuration file (e.g., `~/.bashrc`, `~/.zshrc`, or `~/.profile`).
    *   Add the following lines to the file, replacing `'your_api_key_here'` with the actual API key you obtained:

    ```bash
    export GOOGLE_API_KEY='your_api_key_here'
    export GEMINI_API_KEY='your_api_key_here'
    ```
    
    *   It is highly recommended to set both `GOOGLE_API_KEY` and `GEMINI_API_KEY` to the same value for maximum compatibility and robustness.
    
    *   Save the file and then source it to apply the changes to your current terminal session:
    
    ```bash
    source ~/.bashrc  # Or ~/.zshrc, ~/.profile, etc.
    ```
    
    *   You can verify that the environment variables are set correctly by running:
    
    ```bash
    echo $GOOGLE_API_KEY
    echo $GEMINI_API_KEY
    ```
    
    *   You should see your API key printed in the terminal.

**Important**: Never commit your API key directly into your code or public repositories. Environment variables are the recommended way to handle sensitive information like API keys.

## Usage
After installing the dependencies, you can run the main functionality by executing the `run.py` script from the project root:

```bash
python run.py
```

## Contributing
Contributions are welcome! If you have suggestions for improvements or new features, please feel free to submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.