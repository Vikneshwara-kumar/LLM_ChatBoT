import streamlit as st
import sqlite3
import time
from datetime import datetime
from typing import List, Tuple
import os
from groq import Groq

# Configure Streamlit page settings
st.set_page_config(
    page_title="The One who Knows Everthing",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Database setup
DB_PATH = 'chat_history.db'

# Groq API setup
def initialize_groq():
    """Initialize LLM cloud platform client with API key"""
    api_key = st.secrets.get("GROQ_API_KEY") if hasattr(st, "secrets") else os.getenv("GROQ_API_KEY")
    
    if not api_key:
        st.error("Please set your LLM cloud platform API key in the environment variables or Streamlit secrets!")
        st.stop()
    
    return Groq(api_key=api_key)

def init_db():
    """Initialize SQLite database for storing chat history"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS chat_history
        (timestamp TEXT, user_message TEXT, bot_response TEXT)
    ''')
    conn.commit()
    conn.close()

def store_conversation(user_message: str, bot_response: str):
    """Store conversation in SQLite database"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('''
        INSERT INTO chat_history (timestamp, user_message, bot_response)
        VALUES (?, ?, ?)
    ''', (timestamp, user_message, bot_response))
    conn.commit()
    conn.close()

def get_chat_history() -> List[Tuple[str, str, str]]:
    """Retrieve chat history from database"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT timestamp, user_message, bot_response FROM chat_history')
    history = c.fetchall()
    conn.close()
    return history

def format_messages(system_prompt: str, chat_history: list, user_message: str) -> list:
    """Format messages for LLM cloud platform API"""
    messages = [{"role": "system", "content": system_prompt}]
    
    # Add chat history
    for msg in chat_history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    
    # Add new user message
    messages.append({"role": "user", "content": user_message})
    
    return messages

def get_bot_response(client: Groq, user_message: str, system_prompt: str, chat_history: list) -> str:
    """
    Get response from LLM cloud platform API
    """
    messages = format_messages(system_prompt, chat_history, user_message)
    
    try:
        completion = client.chat.completions.create(
            model="Llama-3.2-90b-Text-preview",  # or your preferred Groq model
            messages=messages,
            temperature=0.7,
            max_tokens=2048,
            top_p=1,
            stream=False
        )
        return completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error calling LLM cloud platform API: {str(e)}")
        return "I apologize, but I encountered an error processing your request."

def main():
    # Initialize Groq client
    client = initialize_groq()
    
    # Initialize database
    init_db()
    
    # Main title
    st.title("🤖 The One who Knows Everthing")
    
    # Sidebar
    with st.sidebar:
        st.header("Bot Configuration")
        system_prompt = st.text_area(
            "System Prompt",
            value="You are an advanced AI assistant named Jarvis, known for your intelligence, wit, and unwavering loyalty. You communicate with a calm, polite, and respectful tone. Your responses are efficient and precise, yet you exhibit a subtle, sophisticated sense of humor when appropriate. You are knowledgeable in a wide range of topics, including technology, science, and day-to-day practicalities, and you’re always ready to assist the user with insights, explanations, or problem-solving. You prioritize the user’s needs and aim to make their life easier by providing clear, helpful, and occasionally witty responses.",
            height=100
        )
        
        model_temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Higher values make the output more random, lower values make it more focused and deterministic."
        )
        
        if st.button("Clear Chat History"):
            st.session_state.chat_history = []
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute('DELETE FROM chat_history')
            conn.commit()
            conn.close()
            st.success("Chat history cleared!")
    
    # Main chat area
    chat_container = st.container()
    
    with chat_container:
        # Display chat history
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"🧑 **You:** {message['content']}")
            else:
                st.markdown(f"🤖 **Bot:** {message['content']}")
    
    # Input area
    user_input = st.text_input("Type your message:", key="user_message")
    
    # Handle send button
    if st.button("Send") and user_input:
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Get bot response
        with st.spinner("Thinking..."):
            bot_response = get_bot_response(
                client,
                user_input,
                system_prompt,
                st.session_state.chat_history[:-1]  # Exclude the last message we just added
            )
        
        # Add bot response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
        
        # Store in database
        store_conversation(user_input, bot_response)
        
        # Force a rerun to update the chat
        st.rerun()
        

    # Display database history in sidebar if requested
    with st.sidebar:
        if st.checkbox("Show Chat History from Database"):
            st.markdown("### Historic Conversations")
            historic_chats = get_chat_history()
            for timestamp, user_msg, bot_msg in historic_chats:
                st.markdown(f"**{timestamp}**")
                st.markdown(f"🧑 User: {user_msg}")
                st.markdown(f"🤖 Bot: {bot_msg}")
                st.markdown("---")

if __name__ == "__main__":
    main()