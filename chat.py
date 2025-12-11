import streamlit as st
from streamlit_chat import message # A commonly used component for chat bubbles
import random
import time

# --- 1. SET PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Simple Streamlit Chatbot",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. INITIALIZE SESSION STATE ---
# Streamlit runs the script from top to bottom on every interaction.
# st.session_state is necessary to preserve the chat history and other variables.
if 'generated' not in st.session_state:
    st.session_state['generated'] = ["Hello! I am a basic chatbot. Ask me something."] # Bot's responses
if 'past' not in st.session_state:
    st.session_state['past'] = ["Hi there!"] # User's inputs

# --- 3. BOT RESPONSE LOGIC ---
def generate_response(prompt):
    """
    Generates a dummy response based on the user's input.
    Replace this with your actual AI logic (e.g., calling an OpenAI or Gemini API).
    """
    prompt_lower = prompt.lower()
    
    if "hello" in prompt_lower or "hi" in prompt_lower:
        return "Greetings! How can I assist you today?"
    elif "name" in prompt_lower:
        return "I am a simple Streamlit chatbot template."
    elif "python" in prompt_lower or "streamlit" in prompt_lower:
        return "Python and Streamlit are great for building web apps quickly!"
    else:
        responses = [
            "That's an interesting question.",
            "I'm not sure how to answer that yet, but I'm learning!",
            "Could you try rephrasing your question?",
            "Tell me more about what you're trying to achieve."
        ]
        return random.choice(responses)

# --- 4. MAIN APPLICATION INTERFACE ---
st.title("Streamlit Chat Demo")

# Create a container for the chat history
response_container = st.container()

# Create a container for the user input
input_container = st.container()

with input_container:
    # Get user input
    user_input = st.text_input("You: ", placeholder="Type your message here...", key="input")
    
    # Handle the submission
    if st.button("Send", key="send_button") and user_input:
        
        # 1. Store user message
        st.session_state.past.append(user_input)
        
        # Simulate thinking time
        with st.spinner("Bot is thinking..."):
            time.sleep(0.5)
            # 2. Generate and store bot response
            output = generate_response(user_input)
            st.session_state.generated.append(output)

        # Force rerun to update chat history
        st.rerun()

# --- 5. DISPLAY CHAT HISTORY ---
with response_container:
    # Reverse the order to display newest message at the bottom
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated']) - 1, -1, -1):
            # Display bot message on the left (True)
            message(st.session_state["generated"][i], key=str(i) + '_generated')
            # Display user message on the right (False)
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
