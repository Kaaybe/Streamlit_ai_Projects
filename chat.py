import streamlit as st
import random
import time

# --- 1. SET PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Streamlit Native Chatbot",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. INITIALIZE SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am a basic chatbot. Ask me something."}
    ]

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


# --- 4. DISPLAY CHAT HISTORY ---
st.title("Streamlit Chat Demo (Native)")

# Display all messages from session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# --- 5. HANDLE USER INPUT ---
if prompt := st.chat_input("Type your message here..."):
    
    # 1. Store user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display the user message immediately
    with st.chat_message("user"):
        st.write(prompt)

    # 2. Generate and store bot response
    with st.chat_message("assistant"):
        with st.spinner("Bot is thinking..."):
            time.sleep(0.5)
            response = generate_response(prompt)
            st.write(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})

# Note: st.chat_input handles rerunning the app automatically.
