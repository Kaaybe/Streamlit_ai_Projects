import streamlit as st
import random
import time
from datetime import datetime

# --- 1. SET PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Assistant Pro",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- 2. CUSTOM CSS FOR BETTER STYLING ---
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stChatMessage {
        background-color: #1e2127;
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
    }
    .chat-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .stat-box {
        background-color: #1e2127;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. INITIALIZE SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "conversation_count" not in st.session_state:
    st.session_state.conversation_count = 0
    
if "bot_personality" not in st.session_state:
    st.session_state.bot_personality = "friendly"
    
if "typing_speed" not in st.session_state:
    st.session_state.typing_speed = 0.03

# --- 4. SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.title("⚙️ Settings")
    
    # Bot personality selector
    st.session_state.bot_personality = st.selectbox(
        "Bot Personality",
        ["friendly", "professional", "humorous", "philosophical"],
        help="Choose how the bot responds"
    )
    
    # Typing speed
    st.session_state.typing_speed = st.slider(
        "Response Speed",
        min_value=0.01,
        max_value=0.1,
        value=0.03,
        help="Adjust typing animation speed"
    )
    
    # Chat statistics
    st.markdown("---")
    st.markdown("### 📊 Chat Stats")
    st.markdown(f"""
        <div class="stat-box">
            <h3>{st.session_state.conversation_count}</h3>
            <p>Messages Sent</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Clear chat button
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.conversation_count = 0
        st.rerun()
    
    # Example prompts
    st.markdown("---")
    st.markdown("### 💡 Try asking:")
    example_prompts = [
        "Tell me a joke",
        "What can you help me with?",
        "Explain quantum computing",
        "Give me a creative writing prompt"
    ]
    for prompt in example_prompts:
        if st.button(prompt, use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.rerun()

# --- 5. ENHANCED BOT RESPONSE LOGIC ---
def generate_response(prompt, personality="friendly"):
    """
    Generates contextually aware responses based on personality and input.
    """
    prompt_lower = prompt.lower()
    
    # Personality-based response modifiers
    personalities = {
        "friendly": {
            "greeting": "Hey there! 👋 How can I brighten your day?",
            "unknown": "That's a fascinating topic! I'd love to explore that with you. 🤔"
        },
        "professional": {
            "greeting": "Good day. How may I assist you?",
            "unknown": "I acknowledge your inquiry. Could you provide more specifics?"
        },
        "humorous": {
            "greeting": "Well, well, well... look who's here! 😄",
            "unknown": "Hmm, my humor circuits are struggling with that one! 🤖"
        },
        "philosophical": {
            "greeting": "Greetings, seeker of knowledge. What wisdom do you pursue?",
            "unknown": "An intriguing question that leads us down the rabbit hole of existence..."
        }
    }
    
    # Context-aware responses
    if any(word in prompt_lower for word in ["hello", "hi", "hey", "greetings"]):
        return personalities[personality]["greeting"]
    
    elif "name" in prompt_lower:
        return f"I'm your AI Assistant Pro! Currently in {personality} mode. 🤖"
    
    elif any(word in prompt_lower for word in ["joke", "funny", "laugh"]):
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything! 😄",
            "I told my computer I needed a break, and now it won't stop sending me Kit-Kat ads! 🍫",
            "Why did the programmer quit his job? He didn't get arrays! 💻",
            "What's a computer's favorite snack? Microchips! 🖥️"
        ]
        return random.choice(jokes)
    
    elif any(word in prompt_lower for word in ["help", "what can you do", "capabilities"]):
        return """I can help you with:
        
• Answering general questions 💬
• Providing creative ideas 💡
• Explaining concepts 📚
• Having engaging conversations 🗨️
• Telling jokes 😄
• And much more!

Just ask me anything, and I'll do my best to assist!"""
    
    elif any(word in prompt_lower for word in ["python", "programming", "code", "streamlit"]):
        return "Ah, a fellow developer! 💻 Python and Streamlit are incredible tools for building interactive apps. Need help with a specific coding question?"
    
    elif any(word in prompt_lower for word in ["time", "date", "day"]):
        now = datetime.now()
        return f"The current time is {now.strftime('%H:%M:%S')} on {now.strftime('%B %d, %Y')} ⏰"
    
    elif any(word in prompt_lower for word in ["weather", "climate"]):
        return "I don't have access to real-time weather data, but I'd recommend checking a weather service for accurate forecasts! ☀️🌧️"
    
    elif "?" in prompt:
        responses = [
            "That's a great question! Let me think about that... 🤔",
            "Interesting inquiry! Here's my perspective: " + random.choice([
                "It depends on various factors and context.",
                "There are multiple ways to approach this.",
                "Let's break this down systematically."
            ]),
            "I appreciate your curiosity! " + personalities[personality]["unknown"]
        ]
        return random.choice(responses)
    
    else:
        return personalities[personality]["unknown"]

# --- 6. TYPING ANIMATION EFFECT ---
def stream_response(response_text):
    """
    Creates a typing animation effect for bot responses.
    """
    message_placeholder = st.empty()
    full_response = ""
    
    for chunk in response_text.split():
        full_response += chunk + " "
        time.sleep(st.session_state.typing_speed)
        message_placeholder.markdown(full_response + "▌")
    
    message_placeholder.markdown(full_response)
    return full_response

# --- 7. MAIN CHAT INTERFACE ---
st.markdown("""
    <div class="chat-header">
        <h1>🤖 AI Assistant Pro</h1>
        <p>Your intelligent conversation partner</p>
    </div>
""", unsafe_allow_html=True)

# Display welcome message if no chat history
if len(st.session_state.messages) == 0:
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown("""
        👋 **Welcome!** I'm your AI Assistant Pro.
        
        I'm here to help answer questions, brainstorm ideas, or just chat. 
        
        *Try selecting different personalities in the sidebar!*
        """)

# Display all messages from session state
for message in st.session_state.messages:
    avatar = "🤖" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.write(message["content"])

# --- 8. HANDLE USER INPUT ---
if prompt := st.chat_input("Type your message here..."):
    # Increment conversation counter
    st.session_state.conversation_count += 1
    
    # Store and display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.write(prompt)
    
    # Generate and display bot response with typing effect
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking..."):
            time.sleep(0.5)  # Brief pause for realism
            response = generate_response(prompt, st.session_state.bot_personality)
            displayed_response = stream_response(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
