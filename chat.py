import streamlit as st
import random
import time
from datetime import datetime

# --- 1. SET PAGE CONFIGURATION ---
st.set_page_config(
    page_title="StudyBuddy AI",
    page_icon="📚",
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
        margin: 10px 0;
    }
    .subject-badge {
        display: inline-block;
        padding: 5px 10px;
        margin: 2px;
        border-radius: 15px;
        background-color: #667eea;
        color: white;
        font-size: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. INITIALIZE SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "study_sessions" not in st.session_state:
    st.session_state.study_sessions = 0
    
if "questions_answered" not in st.session_state:
    st.session_state.questions_answered = 0
    
if "current_subject" not in st.session_state:
    st.session_state.current_subject = "General"
    
if "study_mode" not in st.session_state:
    st.session_state.study_mode = "homework_help"

# --- 4. SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.title("📚 Study Settings")
    
    # Study mode selector
    st.session_state.study_mode = st.selectbox(
        "Study Mode",
        ["homework_help", "exam_prep", "concept_explanation", "quiz_me"],
        format_func=lambda x: {
            "homework_help": "📝 Homework Help",
            "exam_prep": "📖 Exam Preparation",
            "concept_explanation": "💡 Concept Explanation",
            "quiz_me": "🎯 Quiz Me"
        }[x]
    )
    
    # Subject selector
    st.session_state.current_subject = st.selectbox(
        "Current Subject",
        ["General", "Mathematics", "Science", "English", "History", "Programming", "Languages"],
        help="Select your current study subject"
    )
    
    # Study statistics
    st.markdown("---")
    st.markdown("### 📊 Study Stats")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
            <div class="stat-box">
                <h3>🎓 {st.session_state.study_sessions}</h3>
                <p>Study Sessions</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="stat-box">
                <h3>💬 {st.session_state.questions_answered}</h3>
                <p>Questions Asked</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Quick actions
    st.markdown("---")
    st.markdown("### ⚡ Quick Actions")
    
    if st.button("🎯 Start Study Session", use_container_width=True):
        st.session_state.study_sessions += 1
        welcome_msg = f"Great! Let's start a {st.session_state.current_subject} study session. What would you like to work on?"
        st.session_state.messages.append({"role": "assistant", "content": welcome_msg})
        st.rerun()
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    # Study tips and examples
    st.markdown("---")
    st.markdown("### 💡 Example Questions")
    
    example_prompts = {
        "Mathematics": [
            "Help me solve quadratic equations",
            "Explain calculus derivatives",
            "How do I factor polynomials?"
        ],
        "Science": [
            "Explain photosynthesis",
            "What is Newton's third law?",
            "Help me understand the periodic table"
        ],
        "English": [
            "Help me write an essay outline",
            "Explain metaphors and similes",
            "Grammar tips for better writing"
        ],
        "Programming": [
            "Explain Python loops",
            "Help me debug my code",
            "What are functions in programming?"
        ],
        "General": [
            "Create a study schedule",
            "Tips for better note-taking",
            "How to prepare for exams"
        ]
    }
    
    current_examples = example_prompts.get(st.session_state.current_subject, example_prompts["General"])
    for prompt in current_examples:
        if st.button(prompt, use_container_width=True, key=prompt):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.rerun()

# --- 5. STUDENT-FOCUSED RESPONSE LOGIC ---
def generate_student_response(prompt, subject, mode):
    """
    Generates educational responses tailored for students.
    """
    prompt_lower = prompt.lower()
    
    # Greetings
    if any(word in prompt_lower for word in ["hello", "hi", "hey", "start"]):
        greetings = [
            f"Hello! 📚 Ready to tackle some {subject} today? I'm here to help!",
            f"Hey there, scholar! 🎓 What {subject} topic shall we explore?",
            f"Hi! Let's make {subject} easier together. What do you need help with?"
        ]
        return random.choice(greetings)
    
    # Homework help
    elif any(word in prompt_lower for word in ["homework", "assignment", "problem"]):
        return """I'm here to help with your homework! 📝

Here's how we can work together:

1. **Explain the problem** - Tell me what you're working on
2. **Show your work** - Share what you've tried so far
3. **Ask specific questions** - Where are you getting stuck?

Remember: I'll guide you through the solution rather than just giving you the answer. This helps you learn! 💡

What specific homework problem are you working on?"""
    
    # Exam preparation
    elif any(word in prompt_lower for word in ["exam", "test", "quiz", "prepare", "study"]):
        return """Let's prepare for your exam! 📖

**Effective Study Strategy:**

• **Review Key Concepts** - Go through main topics first
• **Practice Problems** - Work through sample questions
• **Create Summaries** - Make notes in your own words
• **Test Yourself** - Use flashcards or practice tests
• **Study in Chunks** - Take breaks every 25-30 minutes

What subject is your exam on? I can help you create a study plan or quiz you on the material!"""
    
    # Mathematics help
    elif any(word in prompt_lower for word in ["math", "calculate", "equation", "algebra", "geometry", "calculus"]):
        return """Let's work on this math problem together! 🔢

**Problem-Solving Steps:**

1. **Understand** - What are we trying to find?
2. **Plan** - What method or formula should we use?
3. **Solve** - Work through step-by-step
4. **Check** - Does our answer make sense?

Tell me the specific problem, and I'll guide you through each step. Remember to show your work - it helps identify where you might need extra support!"""
    
    # Science help
    elif any(word in prompt_lower for word in ["science", "biology", "chemistry", "physics", "experiment"]):
        return """Science questions are my favorite! 🔬

I can help you with:

• **Understanding concepts** - Breaking down complex ideas
• **Lab work** - Understanding experiments and results
• **Formulas & equations** - When and how to use them
• **Real-world applications** - Why this matters

What science topic are you studying? Let's explore it together!"""
    
    # Writing help
    elif any(word in prompt_lower for word in ["essay", "write", "writing", "paragraph", "paper"]):
        return """Let's work on your writing! ✍️

**Essay Writing Framework:**

1. **Brainstorm** - Gather your ideas
2. **Outline** - Organize your thoughts
   - Introduction (hook + thesis)
   - Body paragraphs (evidence + analysis)
   - Conclusion (summary + impact)
3. **Draft** - Write freely, edit later
4. **Revise** - Improve clarity and flow
5. **Proofread** - Fix grammar and spelling

What type of writing assignment are you working on? What's your topic?"""
    
    # Programming help
    elif any(word in prompt_lower for word in ["code", "programming", "python", "javascript", "debug"]):
        return """Let's tackle this coding challenge! 💻

**Debugging Strategy:**

1. **Read the error message** - What is it telling you?
2. **Check syntax** - Are there typos or missing characters?
3. **Trace the logic** - Walk through your code line by line
4. **Test small pieces** - Break down the problem
5. **Use print statements** - See what's happening

Share your code or describe the problem, and we'll debug it together!"""
    
    # Study tips
    elif any(word in prompt_lower for word in ["tip", "how to study", "learn better", "focus"]):
        return """Here are proven study techniques! 🎯

**Study Smart, Not Just Hard:**

• **Pomodoro Technique** - 25 min focus, 5 min break
• **Active Recall** - Test yourself instead of re-reading
• **Spaced Repetition** - Review material over time
• **Teach Someone** - Explaining helps you understand
• **Remove Distractions** - Phone away, focused environment
• **Stay Healthy** - Sleep, exercise, and eat well

Which study technique would you like to try first?"""
    
    # Time management
    elif any(word in prompt_lower for word in ["schedule", "time", "manage", "organize", "plan"]):
        return """Let's create a study schedule! 📅

**Time Management Tips:**

• **Prioritize tasks** - Urgent vs Important
• **Set specific goals** - "Read Chapter 5" not "Study biology"
• **Use a planner** - Digital or paper, whatever works
• **Break big tasks** - Into smaller, manageable chunks
• **Build in buffer time** - Things take longer than expected

What assignments or exams do you have coming up? I can help you plan!"""
    
    # Motivation
    elif any(word in prompt_lower for word in ["tired", "stressed", "difficult", "hard", "give up", "can't"]):
        return """I know studying can be tough, but you've got this! 💪

**Remember:**

• Every expert was once a beginner
• Mistakes are part of learning
• Taking breaks is productive, not lazy
• Progress > Perfection
• You're capable of more than you think!

Take a deep breath. Break the problem into smaller steps. What specific part is challenging you? Let's tackle it together, one step at a time. 🌟"""
    
    # Quiz mode
    elif mode == "quiz_me" or "quiz" in prompt_lower:
        quiz_topics = {
            "Mathematics": "algebra, geometry, or calculus",
            "Science": "biology, chemistry, or physics concepts",
            "English": "grammar, vocabulary, or literary devices",
            "History": "important events and dates",
            "Programming": "coding concepts and syntax"
        }
        topic = quiz_topics.get(subject, "general knowledge")
        return f"Quiz mode activated! 🎯 I can quiz you on {topic}. What specific topic would you like to be quizzed on? Let me know and I'll create some practice questions for you!"
    
    # General questions
    elif "?" in prompt:
        return f"Great question about {subject}! 🤔 Let me help you understand this better. Could you provide a bit more detail about what specifically you'd like to know? The more context you give, the better I can assist you!"
    
    # Default response
    else:
        return f"""I'm here to help with your {subject} studies! 📚

I can assist with:
• Explaining difficult concepts
• Solving problems step-by-step
• Creating study plans
• Preparing for exams
• Checking your work
• Providing study tips

What would you like to work on today?"""

# --- 6. TYPING ANIMATION EFFECT ---
def stream_response(response_text):
    """Creates a typing animation effect for bot responses."""
    message_placeholder = st.empty()
    full_response = ""
    
    for chunk in response_text.split():
        full_response += chunk + " "
        time.sleep(0.02)
        message_placeholder.markdown(full_response + "▌")
    
    message_placeholder.markdown(full_response)
    return full_response

# --- 7. MAIN CHAT INTERFACE ---
st.markdown("""
    <div class="chat-header">
        <h1>📚 StudyBuddy AI</h1>
        <p>Your Personal Study Assistant</p>
    </div>
""", unsafe_allow_html=True)

# Display current subject badge
st.markdown(f'<span class="subject-badge">📖 Current: {st.session_state.current_subject}</span>', unsafe_allow_html=True)

# Display welcome message if no chat history
if len(st.session_state.messages) == 0:
    with st.chat_message("assistant", avatar="🎓"):
        st.markdown(f"""
        👋 **Welcome to StudyBuddy AI!**
        
        I'm your personal study assistant, here to help you:
        
        • 📝 Complete homework and assignments
        • 📖 Prepare for exams
        • 💡 Understand difficult concepts
        • ✍️ Improve your writing
        • 🎯 Stay organized and motivated
        
        **Current Subject:** {st.session_state.current_subject}
        
        *What would you like to work on today?*
        """)

# Display all messages from session state
for message in st.session_state.messages:
    avatar = "🎓" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.write(message["content"])

# --- 8. HANDLE USER INPUT ---
if prompt := st.chat_input("Ask a question or describe what you need help with..."):
    # Increment counters
    st.session_state.questions_answered += 1
    
    # Store and display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.write(prompt)
    
    # Generate and display bot response with typing effect
    with st.chat_message("assistant", avatar="🎓"):
        with st.spinner("Thinking... 💭"):
            time.sleep(0.5)
            response = generate_student_response(
                prompt, 
                st.session_state.current_subject,
                st.session_state.study_mode
            )
            displayed_response = stream_response(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
