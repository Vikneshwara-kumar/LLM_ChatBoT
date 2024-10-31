
# The One Who Knows Everything 🤖

## Video Demo

<video width="600" controls>
  <source src="https://github.com/Vikneshwara-kumar/LLM_ChatBoT/blob/main/Demo.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

## Table of Contents
1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Code Structure](#code-structure)
6. [Contributing](#contributing)
7. [License](#license)
8. [Acknowledgements](#acknowledgements)

## Features

- **Chat Interface**: An intuitive user interface for interacting with the AI assistant.
- **Persistent Chat History**: Stores and retrieves chat history using SQLite.
- **Customizable System Prompt**: Allows users to configure the assistant's behavior and personality through a customizable system prompt.
- **Temperature Control**: Adjusts the randomness of the assistant's responses.
- **Clear Chat History**: Option to clear the chat history both from the session and the database.
- **View Historic Conversations**: Sidebar feature to view past conversations stored in the database.

## Prerequisites

- Python 3.7 or higher
- Streamlit
- SQLite3
- Groq API key (for LLM integration)

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/Vikneshwara-kumar/LLM_ChatBoT.git
   cd the-one-who-knows-everything
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variable or Streamlit secrets for the Groq API key:

   ```bash
   export GROQ_API_KEY='your_api_key_here'
   ```

   Or create a `.streamlit/secrets.toml` file with the following content:

   ```toml
   mkdir .streamlit
   echo "GROQ_API_KEY = 'your-api-key-here'" > .streamlit/secrets.toml
   ```

4. Run the Streamlit application:

   ```bash
   streamlit run app.py
   ```

## Usage

1. Open the application in your web browser (the default URL is usually `http://localhost:8501`).
2. Enter your message in the text input field and click "Send" to get a response from the assistant.
3. Use the sidebar to configure the system prompt, adjust the response temperature, and view or clear chat history.

## Code Structure

- **app.py**: Main application file containing the Streamlit app code.
- **initialize_groq**: Sets up the Groq API client using the provided API key.
- **init_db**: Initializes the SQLite database and creates a table for storing chat history if it does not exist.
- **store_conversation**: Stores the conversation (user message and bot response) in the database.
- **get_chat_history**: Retrieves the chat history from the database.
- **format_messages**: Formats messages for the LLM API, including the system prompt and chat history.
- **get_bot_response**: Calls the Groq API to get a response from the AI assistant.
- **main**: The main function that sets up the Streamlit app, initializes the Groq client, and handles user input and display of chat history.

## Contributing

Contributions are welcome! If you have suggestions or improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

- [Streamlit](https://streamlit.io/) for creating the web application framework.
- [SQLite](https://www.sqlite.org/) for the lightweight database solution.
- [Groq](https://groq.com/) for providing the LLM cloud platform.

---
