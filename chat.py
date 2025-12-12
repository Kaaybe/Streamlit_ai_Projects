import streamlit as st
import random
import time
from datetime import datetime

# --- 1. SET PAGE CONFIGURATION ---
st.set_page_config(
    page_title="CBC Lesson Generator",
    page_icon="📚",
    layout="wide",
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
    .header-banner {
        text-align: center;
        padding: 30px;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        border-radius: 15px;
        margin-bottom: 20px;
    }
    .stat-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        text-align: center;
    }
    .grade-badge {
        display: inline-block;
        padding: 5px 15px;
        margin: 5px;
        border-radius: 20px;
        background-color: #2a5298;
        color: white;
        font-size: 14px;
        font-weight: bold;
    }
    .subject-tag {
        display: inline-block;
        padding: 8px 16px;
        margin: 5px;
        border-radius: 15px;
        background-color: #667eea;
        color: white;
        font-size: 13px;
    }
    .material-card {
        background-color: #1e2127;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #667eea;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. INITIALIZE SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "materials_generated" not in st.session_state:
    st.session_state.materials_generated = 0

if "current_grade" not in st.session_state:
    st.session_state.current_grade = "Grade 4"

if "current_subject" not in st.session_state:
    st.session_state.current_subject = "Mathematics"

if "material_type" not in st.session_state:
    st.session_state.material_type = "worksheet"

if "user_role" not in st.session_state:
    st.session_state.user_role = "teacher"

# --- 4. CBC CURRICULUM DATA ---
CBC_SUBJECTS = {
    "Lower Primary (Grade 1-3)": [
        "Mathematics", "English", "Kiswahili", "Environmental Activities",
        "Hygiene and Nutrition", "Religious Education", "Movement and Creative Activities"
    ],
    "Upper Primary (Grade 4-6)": [
        "Mathematics", "English", "Kiswahili", "Science and Technology",
        "Social Studies", "Religious Education", "Creative Arts", "Physical Education"
    ],
    "Junior Secondary (Grade 7-9)": [
        "Mathematics", "English", "Kiswahili", "Integrated Science",
        "Social Studies", "Religious Education", "Creative Arts and Sports",
        "Pre-Technical Studies", "Business Studies", "Agriculture"
    ]
}

MATERIAL_TYPES = {
    "worksheet": "📝 Worksheet",
    "lesson_plan": "📋 Lesson Plan",
    "activity": "🎯 Learning Activity",
    "assessment": "✅ Assessment Tool",
    "flashcards": "🎴 Flashcards",
    "project": "🔬 Project Guide",
    "notes": "📖 Study Notes",
    "quiz": "❓ Quiz/Test"
}

# --- 5. SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.title("🎓 CBC Generator Settings")

    # User role selector
    st.session_state.user_role = st.radio(
        "I am a:",
        ["teacher"],
        format_func=lambda x: "👨‍🏫 Teacher" if x == "teacher" else "👨‍🎓 Student"
    )

    st.markdown("---")

    # Grade level selector
    st.session_state.current_grade = st.selectbox(
        "Grade Level",
        ["Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5", "Grade 6",
         "Grade 7", "Grade 8", "Grade 9"],
        index=3
    )

    # Determine curriculum level
    grade_num = int(st.session_state.current_grade.split()[1])
    if grade_num <= 3:
        curriculum_level = "Lower Primary (Grade 1-3)"
    elif grade_num <= 6:
        curriculum_level = "Upper Primary (Grade 4-6)"
    else:
        curriculum_level = "Junior Secondary (Grade 7-9)"

    # Subject selector based on grade
    st.session_state.current_subject = st.selectbox(
        "Subject",
        CBC_SUBJECTS[curriculum_level]
    )

    # Material type selector
    st.session_state.material_type = st.selectbox(
        "Material Type",
        list(MATERIAL_TYPES.keys()),
        format_func=lambda x: MATERIAL_TYPES[x]
    )

    # Statistics
    st.markdown("---")
    st.markdown("### 📊 Generation Stats")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
            <div class="stat-box">
                <h2>📚 {st.session_state.materials_generated}</h2>
                <p>Materials Created</p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="stat-box">
                <h2>💬 {len(st.session_state.messages)//2}</h2>
                <p>Requests Made</p>
            </div>
        """, unsafe_allow_html=True)

    # Quick action buttons
    st.markdown("---")
    st.markdown("### ⚡ Quick Actions")

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    if st.button("📥 Download Materials", use_container_width=True):
        st.info("Download feature coming soon! Materials will be exportable as PDF/Word.")

    # Example prompts
    st.markdown("---")
    st.markdown("### 💡 Example Requests")

    example_prompts = {
        "worksheet": [
            f"Create a {st.session_state.current_subject} worksheet on fractions",
            "Generate practice problems with word problems",
            "Make an illustrated worksheet about shapes"
        ],
        "lesson_plan": [
            f"Write a lesson plan for {st.session_state.current_subject}",
            "Create a 40-minute lesson on photosynthesis",
            "Plan a lesson with group activities"
        ],
        "activity": [
            "Design a hands-on science experiment",
            "Create a group learning activity",
            "Make an interactive classroom game"
        ],
        "assessment": [
            "Generate end of term exam questions",
            "Create a formative assessment tool",
            "Make a rubric for project evaluation"
        ],
        "notes": [
            f"Create study notes on {st.session_state.current_subject} on basic concepts",
            "Generate detailed notes about ecosystems",
            "Summarize the key events of the scramble for Africa"
        ]
    }

    current_examples = example_prompts.get(st.session_state.material_type, example_prompts["worksheet"])
    for prompt in current_examples[:3]:
        if st.button(prompt, use_container_width=True, key=prompt):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.rerun()

# --- 6. CONTENT GENERATION LOGIC ---
def generate_lesson_material(prompt, grade, subject, material_type, role):
    """
    Generates CBC-aligned educational materials based on user input.
    """
    prompt_lower = prompt.lower()

    # 1. Handle special prompts like greetings or help requests first
    if any(word in prompt_lower for word in ["hello", "hi", "hey", "start"]):
        if role == "teacher":
            return f"""👋 **Welcome, Teacher!**\n\nI'm your CBC Lesson Material Generator. I can help you create:\n\n📝 **Worksheets** - Practice exercises with solutions\n📋 **Lesson Plans** - Structured 40-minute lessons\n🎯 **Activities** - Engaging hands-on learning\n✅ **Assessments** - Quizzes, tests, and rubrics\n📖 **Study Notes** - Summaries and revision materials\n\n**Current Settings:**\n- Grade: {grade}\n- Subject: {subject}\n- Material: {MATERIAL_TYPES[material_type]}\n\nWhat would you like me to create today?"""
        else:
            return f"""👋 **Hello, Student!**\n\nI can help you with:\n\n📖 **Study materials** for {subject}\n📝 **Practice worksheets**\n🎯 **Learning activities**\n💡 **Topic explanations**\n\nWhat topic are you studying in {grade}?"""
    elif "help" in prompt_lower or "how" in prompt_lower:
        # Keep existing detailed help text
        if role == "teacher":
            return f"""# 💡 How to Use the CBC Lesson Generator\n\nI can create various learning materials for {grade} {subject}:\n\n## **Available Material Types:**\n\n### 📝 **Worksheets**\nPractice exercises with problems to solve. Great for homework or classwork.\n*Example: "Create a math worksheet on fractions for grade 4"*\n\n### 📋 **Lesson Plans**\nComplete 40-minute lesson plans following CBC format.\n*Example: "Write a lesson plan on photosynthesis"*\n\n### 🎯 **Learning Activities**\nHands-on group activities and experiments.\n*Example: "Design a science experiment about plants"*\n\n### ✅ **Assessments**\nTests, quizzes, and evaluation tools with marking schemes.\n*Example: "Generate an end-of-term test for science"*\n\n### 🎴 **Flashcards**\nStudy cards for revision and quick practice.\n*Example: "Make flashcards for Kiswahili vocabulary"*\n\n### 📖 **Study Notes**\nSummaries and revision materials for students.\n*Example: "Create study notes on Kenyan history"*\n\n---\n\n## **Tips for Best Results:**\n\n1. **Be Specific:** Mention the exact topic you want\n   - ✅ "Create worksheet on adding fractions"\n   - ❌ "Create math worksheet"\n\n2. **Mention Grade Level:** (Already set in sidebar)\n   - Current: {grade}\n\n3. **Include Context:** Tell me about your students' needs\n   - "My students struggle with word problems"\n   - "I need visual aids for this topic"\n\n4. **Request Customization:**\n   - "Make it culturally relevant to Kenya"\n   - "Include local examples"\n   - "Add illustrations"\n\n---\n\n## **Sample Requests:**\n\n- "Create a worksheet on multiplication with Kenyan currency examples"\n- "Write a lesson plan about clean water with hands-on activities"\n- "Generate flashcards for English grammar - present tense"\n- "Make an assessment tool for science - states of matter" \n- "Design a group activity about healthy eating using local foods"\n\n---\n\n**What would you like me to create?**\n"""
        else:
            return f"""# 💡 How I Can Help You Learn\n\nHi! I can help you study {subject} for {grade}. Here's what I can do:\n\n## **I Can Create:**\n\n📖 **Study Notes** - Summaries to help you understand topics better\n\n📝 **Practice Worksheets** - Problems to practice what you've learned\n\n🎴 **Flashcards** - Cards to help you memorize important facts\n\n💡 **Explanations** - Break down difficult concepts into simple terms\n\n---\n\n## **Just Tell Me:**\n\n1. What topic you're studying\n2. What you need help with\n3. What you find difficult\n\n**Examples:**\n- "I need help understanding fractions"\n- "Can you explain photosynthesis simply?"\n- "Make practice problems for multiplication"\n\n---\n\nWhat subject are you studying today?\n"""

    # 2. Extract topic from the prompt, *after* special commands are handled
    #    and based on the *selected* material_type.
    topic_keywords_to_remove = {
        "worksheet": ["worksheet", "create", "generate"],
        "lesson_plan": ["lesson plan", "create", "write"],
        "activity": ["activity", "create", "design"],
        "assessment": ["test", "exam", "quiz", "assessment", "create", "generate"],
        "flashcards": ["flashcard", "flashcards", "create", "make"],
        "notes": ["study notes", "notes", "create", "generate", "explain", "summarize"]
    }

    current_prompt_for_topic = prompt_lower
    # Remove material-type-specific keywords from the prompt to isolate the topic
    if material_type in topic_keywords_to_remove:
        for keyword in topic_keywords_to_remove[material_type]:
            current_prompt_for_topic = current_prompt_for_topic.replace(keyword, "")
    
    # Also remove generic action verbs if they remain and are not part of the topic
    for generic_word in ["about", "on", "for", "a", "an", "the"]: # Added more common generic words
        # Ensure we're removing whole words, not just parts of words
        if current_prompt_for_topic.startswith(generic_word + " "):
            current_prompt_for_topic = current_prompt_for_topic[len(generic_word) + 1:].strip()
        if current_prompt_for_topic.endswith(" " + generic_word):
            current_prompt_for_topic = current_prompt_for_topic[:-len(generic_word) - 1].strip()


    topic = current_prompt_for_topic.strip()

    if not topic or len(topic) < 3:
        topic = "the current topic"

    # 3. Generate material based *strictly* on the `material_type` from the sidebar
    if material_type == "worksheet":
        return f"""# 📝 **{subject} Worksheet - {grade}**\n**Topic: {topic.title()}**\n\n---\n\n## **Part A: Understanding the Concept** (10 marks)\n\n**Instructions:** Answer the following questions in the spaces provided.\n\n1. Define or explain what {topic} means in your own words.\n\n   ____________________________________________________________\n\n   ____________________________________________________________\n\n2. Give TWO real-life examples where you can observe or use {topic}.\n\n   a) ____________________________________________________________\n\n   b) ____________________________________________________________\n\n3. Why is understanding {topic} important? Write one reason.\n\n   ____________________________________________________________\n\n---\n\n## **Part B: Practice Problems** (20 marks)\n\n**Instructions:** Solve the following problems. Show your working.\n\n**Question 1:** [Context-based problem related to {topic}]\n\n_Working space:_\n\n\n\n\n**Question 2:** [Progressive difficulty problem]\n\n_Working space:_\n\n\n\n\n**Question 3:** [Application problem using local context]\n\n_Working space:_\n\n\n\n\n---\n\n## **Part C: Challenge Section** (10 marks)\n\n**Critical Thinking:**\n\n1. How would you explain {topic} to a younger student? Write a simple explanation.\n\n____________________________________________________________\n\n____________________________________________________________\n\n2. Create your own problem about {topic} using things from your environment.\n\n____________________________________________________________\n\n____________________________________________________________\n\n---\n\n## **Teacher's Notes:**\n\n✅ **Learning Outcomes:** Students will be able to:\n- Understand the concept of {topic}\n- Apply knowledge to solve problems\n- Make connections to real-life situations\n\n📊 **Assessment Criteria:**\n- Understanding: 10 marks\n- Problem-solving: 20 marks\n- Critical thinking: 10 marks\n- **Total: 40 marks**\n\n🎯 **Differentiation:**\n- Support struggling learners with Part A\n- Challenge advanced learners with Part C\n- Use group work for collaborative learning\n\n---\n\n*Generated for {grade} - {subject} | CBC Aligned*\n"""

    elif material_type == "lesson_plan":
        return f"""📋 **LESSON PLAN**\n**{subject} - {grade}**\n\n---\n\n**Topic:** {topic.title()}\n**Date:** ________________\n**Duration:** 40 minutes\n**Class Size:** ______\n\n---\n\n## **1. LEARNING OUTCOMES** 🎯\n\nBy the end of the lesson, learners should be able to:\n- [ ] Explain the concept of {topic}\n- [ ] Apply knowledge to solve related problems\n- [ ] Demonstrate understanding through practical activities\n- [ ] Work collaboratively with peers\n\n**Specific Competencies Addressed:**\n- Communication and collaboration\n- Critical thinking and problem-solving\n- Learning to learn\n\n---\n\n## **2. LEARNING RESOURCES** 📚\n\n**Materials Needed:**\n- Textbooks/reference materials\n- Writing materials (pens, pencils, exercise books)\n- Manila papers/chart papers\n- [Specific materials for {topic}]\n- Locally available resources (e.g., stones, sticks, bottle tops)\n\n**Prerequisite Knowledge:**\nStudents should have prior knowledge of [related foundational concepts]\n\n---\n\n## **3. LESSON STRUCTURE** ⏰\n\n### **Introduction (5 minutes)**\n- Greet learners and settle the class\n- Recap previous lesson briefly\n- Introduce today's topic: {topic}\n- Ask thought-provoking question: "Have you ever wondered about...?"\n- State learning objectives clearly\n\n### **Lesson Development (25 minutes)**\n\n**Activity 1: Teacher Explanation (8 minutes)**\n- Explain the concept of {topic} using simple language\n- Use examples from learners' environment\n- Draw diagrams or illustrations on the board\n- Ask questions to check understanding\n\n**Activity 2: Guided Practice (10 minutes)**\n- Demonstrate a problem/activity related to {topic}\n- Guide learners through solving similar problems\n- Move around the class to assist individuals\n- Encourage peer teaching\n\n**Activity 3: Group Activity (7 minutes)**\n- Divide class into groups of 4-5\n- Give each group a task related to {topic}\n- Provide materials for hands-on activity\n- Monitor group progress and participation\n\n### **Conclusion (10 minutes)**\n- Groups present their findings (2-3 groups)\n- Summarize key points of the lesson\n- Link back to learning objectives\n- Give homework/assignment\n- Preview next lesson\n\n---\n\n## **4. ASSESSMENT METHODS** ✅\n\n**Formative Assessment:**\n- Observation during group work\n- Oral questions throughout the lesson\n- Quick quiz at the end\n\n**Questions to Ask:**\n1. What have we learned about {topic}?\n2. Can someone give an example from our environment?\n3. How can we apply this in our daily lives?\n\n**Homework Assignment:**\n[Related practice exercise or project]\n\n---\n\n## **5. DIFFERENTIATION STRATEGIES** 🎨\n\n**For Struggling Learners:**\n- Provide additional visual aids\n- Pair with peer tutor\n- Give simpler problems\n- Offer more time\n\n**For Advanced Learners:**\n- Assign extension activities\n- Give leadership roles in groups\n- Provide challenging problems\n- Encourage independent research\n\n---\n\n## **6. REFLECTION** 💭\n\n**After the lesson, reflect on:**\n- Were learning outcomes achieved?\n- Which activities worked well?\n- What needs improvement?\n- Did all learners participate?\n- Time management effectiveness\n\n**Notes:**\n_____________________________________________________________\n\n_____________________________________________________________\n\n---\n\n*Prepared for {grade} - {subject} | CBC Aligned*\n*This lesson plan follows the Competency-Based Curriculum framework*\n"""

    elif material_type == "activity":
        return f"""🎯 **LEARNING ACTIVITY**\n**{subject} - {grade}**\n\n---\n\n**Activity Title:** Exploring **{topic.title()}**\n**Duration:** 30-40 minutes\n**Group Size:** 4-5 learners per group\n\n---\n\n## **LEARNING OBJECTIVES** 🎓\n\nLearners will:\n1. Actively engage with concepts related to {topic}\n2. Collaborate with peers to solve problems\n3. Apply critical thinking skills\n4. Demonstrate understanding through hands-on work\n\n---\n\n## **MATERIALS NEEDED** 📦\n\n- Manila paper or chart paper (1 per group)\n- Markers/crayons/colored pencils\n- Exercise books for recording\n- [Specific items for {topic} - use local materials]\n- Examples: bottle tops, stones, seeds, sticks, newspapers\n\n---\n\n## **ACTIVITY INSTRUCTIONS** 📝\n\n### **Step 1: Introduction (5 minutes)**\n- Teacher explains the activity objectives\n- Demonstrate what students will do\n- Divide class into groups\n- Assign roles: Leader, Recorder, Presenter, Materials Manager\n\n### **Step 2: Main Activity (20-25 minutes)**\n\n**Task for Groups:**\n\nYour group will explore {topic} by:\n\n1. **Discuss** (5 minutes)\n   - What do you know about {topic}?\n   - Share ideas within your group\n   - Write down key points\n\n2. **Create/Experiment** (10-15 minutes)\n   - Use the materials provided\n   - Design a model/chart/experiment about {topic}\n   - Work together - everyone contributes!\n   - Record your observations\n\n3. **Prepare Presentation** (5 minutes)\n   - Organize your findings\n   - Choose who will present\n   - Practice explaining your work\n\n### **Step 3: Presentations (10 minutes)**\n- Each group presents (2-3 minutes per group)\n- Other groups ask questions\n- Teacher provides feedback\n\n---\n\n## **GUIDING QUESTIONS** ❓\n\nHelp your group think about:\n- What did you discover about {topic}?\n- How does this relate to our daily lives?\n- What challenges did you face?\n- What would you do differently?\n- How can you use this knowledge?\n\n---\n\n## **ASSESSMENT CRITERIA** ✅\n\nGroups will be assessed on:\n\n| Criteria | Points |\n|----------|--------|\n| Participation of all members | 5 |\n| Understanding of {topic} | 5 |\n| Creativity and effort | 5 |\n| Presentation quality | 5 |\n| **Total** | **20** |\n\n---\n\n## **EXTENSION ACTIVITIES** 🌟\n\n**For Fast Finishers:**\n- Research more about {topic} using library books\n- Create a poster to display in class\n- Teach the concept to another student\n\n**Home Connection:**\n- Find examples of {topic} at home\n- Discuss with family members\n- Bring an item related to {topic} for next class\n\n---\n\n## **TEACHER NOTES** 📌\n\n**Preparation:**\n- Collect all materials before the lesson\n- Arrange classroom for group work\n- Prepare sample to show students\n\n**During Activity:**\n- Circulate and observe all groups\n- Ask probing questions\n- Assist struggling groups\n- Take photos for documentation\n\n**Safety Considerations:**\n- [List any safety rules relevant to the activity]\n\n**Differentiation:**\n- Provide extra support to groups that need it\n- Give more complex tasks to advanced learners\n- Allow different ways of presenting\n\n---\n\n*Activity designed for {grade} - {subject} | CBC Aligned*\n*Promotes hands-on learning and collaboration*\n"""

    elif material_type == "assessment" or material_type == "quiz":
        return f"""✅ **ASSESSMENT TOOL**\n**{subject} - {grade}**\n**{topic.title()}**\n\n---\n\n**Name:** ______________________________  **Date:** ______________\n\n**Class:** ________  **Time Allowed:** 60 minutes\n\n**Total Marks:** 50\n\n---\n\n## **INSTRUCTIONS** 📋\n\n1. Answer ALL questions in the spaces provided\n2. Write your name and class clearly\n3. Show all your working\n4. Check your answers before submitting\n5. Write neatly and legibly\n\n---\n\n## **SECTION A: Multiple Choice** (10 marks)\n\nChoose the correct answer and write the letter in the brackets.\n\n1. Which of the following best describes {topic}?\n   - A) Option one\n   - B) Option two\n   - C) Option three\n   - D) Option four\n
   Answer: [ ]\n\n2. [Question about {topic}]\n   - A)\n   - B)\n   - C)\n   - D)\n
   Answer: [ ]\n\n3-10. [Continue with similar format]\n\n---\n\n## **SECTION B: Short Answer Questions** (15 marks)\n\nAnswer the following questions briefly.\n\n1. Define {topic} in your own words. (3 marks)\n\n   ____________________________________________________________\n\n   ____________________________________________________________\n\n   ____________________________________________________________\n\n2. Give THREE examples of {topic} from your environment. (3 marks)\n\n   a) ____________________________________________________________\n\n   b) ____________________________________________________________\n\n   c) ____________________________________________________________\n\n3. Explain why {topic} is important in our daily lives. (4 marks)\n\n   ____________________________________________________________\n\n   ____________________________________________________________\n\n   ____________________________________________________________\n\n   ____________________________________________________________\n\n4. List TWO ways you can apply knowledge of {topic}. (2 marks)\n\n   a) ____________________________________________________________\n\n   b) ____________________________________________________________\n\n5. What challenges might you face when dealing with {topic}? (3 marks)\n\n   ____________________________________________________________\n\n   ____________________________________________________________\n\n---\n\n## **SECTION C: Problem Solving** (15 marks)\n\nSolve the following problems. Show ALL your working clearly.\n\n**Question 1:** (5 marks)\n\n[Context-based problem related to {topic}]\n\n_Working:_\n\n\n\n\n\n_Answer:_ ______________________\n\n**Question 2:** (5 marks)\n\n[Application problem using real-life scenario]\n\n_Working:_\n\n\n\n\n\n_Answer:_ ______________________\n\n**Question 3:** (5 marks)\n\n[Complex problem requiring critical thinking]\n\n_Working:_\n\n\n\n\n\n_Answer:_ ______________________\n\n---\n\n## **SECTION D: Extended Response** (10 marks)\n\n**Question:** Write a short paragraph explaining {topic}. Include:\n- What it is\n- Why it matters\n- How it's used\n- An example from your life\n\nWrite at least 5-7 sentences.\n\n____________________________________________________________\n\n____________________________________________________________\n\n____________________________________________________________\n\n____________________________________________________________\n\n____________________________________________________________\n\n____________________________________________________________\n\n____________________________________________________________\n\n____________________________________________________________\n\n---\n\n## **MARKING SCHEME** (For Teacher Use)\n\n| Section | Marks | Student Score |\n|---------|-------|---------------|\n| Section A: Multiple Choice | 10 | |\n| Section B: Short Answer | 15 | |\n| Section C: Problem Solving | 15 | |\n| Section D: Extended Response | 10 | |\n| **TOTAL** | **50** | |\n\n**Grading Scale:**\n- 45-50: Exceeds Expectations\n- 35-44: Meets Expectations\n- 25-34: Approaches Expectations\n- Below 25: Needs Support\n\n**Teacher Comments:**\n\n____________________________________________________________\n\n____________________________________________________________\n\n---\n\n*Assessment for {grade} - {subject} | CBC Aligned*\n*Covers knowledge, skills, and competencies*\n"""

    elif material_type == "flashcards":
        return f"""🎴 **FLASHCARDS SET**\n**{subject} - {grade}**\n**Topic: {topic.title()}**\n\n---\n\n**Instructions for Teachers:**\n1. Print these flashcards on cardstock\n2. Cut along the dotted lines\n3. Fold in half (question on front, answer on back)\n4. Laminate for durability (optional)\n\n**Ways to Use:**\n- Individual study/revision\n- Pair work (students quiz each other)\n- Group games (quiz competitions)\n- Quick formative assessment\n\n---\n\n## 📇 FLASHCARD 1\n**FRONT (Question):**\n> What is {topic}?\n\n**BACK (Answer):**\n> [Clear, concise definition with example]\n\n---\n\n## 📇 FLASHCARD 2\n**FRONT (Question):**\n> Give an example of {topic} from your daily life.\n\n**BACK (Answer):**\n> [Real-world example relevant to Kenyan context]\n\n---\n\n## 📇 FLASHCARD 3\n**FRONT (Question):**\n> Why is {topic} important?\n\n**BACK (Answer):**\n> [2-3 reasons explaining significance]\n\n---\n\n## 📇 FLASHCARD 4\n**FRONT (Question):**\n> How do you [action related to {topic}]?\n\n**BACK (Answer):**\n> [Step-by-step process or method]\n\n---\n\n## 📇 FLASHCARD 5\n**FRONT (Question):**\n> What tools or materials do you need for {topic}?\n\n**BACK (Answer):**\n> [List of relevant materials/tools]\n\n---\n\n## 📇 FLASHCARD 6\n**FRONT (Question):**\n> Name TWO types or categories of {topic}.\n\n**BACK (Answer):**\n> 1. [Type one with brief description]\n> 2. [Type two with brief description]\n\n---\n\n## 📇 FLASHCARD 7\n**FRONT (Question):**\n> What is the difference between [A] and [B] in {topic}?"\n\n**BACK (Answer):**\n> [Clear comparison highlighting key differences]\n\n---\n\n## 📇 FLASHCARD 8\n**FRONT (Question):**\n> Draw or describe [visual element related to {topic}]\n\n**BACK (Answer):**\n> [Description of expected drawing/diagram with labels]\n\n---\n\n## 📇 FLASHCARD 9\n**FRONT (Question):**\n> True or False: [Statement about {topic}]\n\n**BACK (Answer):**\n> [True/False with explanation why]\n\n---\n\n## 📇 FLASHCARD 10\n**FRONT (Question):**\n> Challenge: How can you apply {topic} to solve a problem in your community?\n\n**BACK (Answer):**\n> [Creative application showing higher-order thinking]\n\n---\n\n**BONUS ACTIVITY IDEAS:**\n
🎯 **Memory Game:** Use two sets of flashcards. Place face down. Students find matching pairs.\n\n🏆 **Quiz Competition:** Divide class into teams. Teams earn points for correct answers.\n\n✏️ **Create Your Own:** Students make their own flashcards about {topic}.\n\n⏱️ **Speed Round:** How many can you answer in 2 minutes?\n\n---\n\n*Flashcards for {grade} - {subject} | CBC Aligned*\n*Print, cut, and laminate for classroom use*\n"""

    elif material_type == "notes":
        return f"""📖 **STUDY NOTES**\n**{subject} - {grade}**\n**Topic: {topic.title()}**\n\n---\n\n**1. Introduction to {topic.title()}**\n\nBrief overview of the topic: What is it? Why is it important?\n\n____________________________________________________________\n____________________________________________________________\n\n**2. Key Definitions & Concepts**\n\n- **[Concept 1]:** [Definition and simple explanation]\n- **[Concept 2]:** [Definition and simple explanation]\n- **[Concept 3]:** [Definition and simple explanation]\n\n**3. Main Ideas & Principles**\n\n- Point 1: [Elaborate on a main idea with examples]\n- Point 2: [Another main idea, perhaps with a diagram or an analogy]\n- Point 3: [Third main idea, how it connects to other concepts]\n\n**4. Examples & Applications**\n\n- **Example 1:** [Real-world example related to {topic}]\n- **Example 2:** [Another example, possibly a local context]\n\n**5. Important Formulas/Diagrams (if applicable)**\n\n[Insert relevant formulas, charts, or diagrams here]\n\n**6. Quick Quiz / Self-Assessment**\n\n1. What is the main idea of {topic}? (Short Answer)\n\n2. Give one example of {topic} that you see every day. (Application)\n\n3. True or False: [Statement related to {topic}] (Concept Check)\n\n**7. Further Reading / Resources**\n\n- [Link to a relevant textbook chapter]\n- [Suggest a video or online article]\n\n---\n\n*Study Notes for {grade} - {subject} | CBC Aligned*\n*Designed for quick revision and understanding*\n"""
    else:
        # Default response if the material_type is unknown or unhandled
        material_name = MATERIAL_TYPES.get(material_type, material_type)
        return f"""I'm sorry, I don't know how to generate '{material_name}' materials yet.\n        Please select one of the available material types from the sidebar.\n\n        **Current Settings:**\n        - Grade: {grade}\n        - Subject: {subject}\n- Material: {MATERIAL_TYPES.get(material_type, 'Unknown')}\n\n        What would you like me to create?"""

# --- 7. TYPING ANIMATION ---
def stream_response(response_text):
    """
    Creates a typing animation effect for responses.
    """
    message_placeholder = st.empty()
    full_response = ""

    # Stream by chunks for better performance
    words = response_text.split()
    chunk_size = 3

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size]) + " "
        full_response += chunk
        time.sleep(0.03)
        message_placeholder.markdown(full_response + "▌")

    message_placeholder.markdown(full_response)
    return full_response

# --- 8. MAIN INTERFACE ---
st.markdown("""
    <div class="header-banner">
        <h1>📚 CBC Lesson Material Generator</h1>
        <p>Create Localized Learning Materials Instantly</p>
    </div>
""", unsafe_allow_html=True)

# Display current settings
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'<div class="grade-badge">Grade: {st.session_state.current_grade}</div>', unsafe_allow_html=True)

with col2:
    st.markdown(f'<div class="subject-tag">Subject: {st.session_state.current_subject}</div>', unsafe_allow_html=True)

with col3:
    material_display_name = MATERIAL_TYPES.get(st.session_state.material_type, st.session_state.material_type)
    st.markdown(f'<div class="grade-badge">Type: {material_display_name}</div>', unsafe_allow_html=True)

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

# Accept user input
if prompt := st.chat_input("What would you like to create?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt, unsafe_allow_html=True)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner("Generating material..."):
            response = generate_lesson_material(
                prompt,
                st.session_state.current_grade,
                st.session_state.current_subject,
                st.session_state.material_type,
                st.session_state.user_role
            )
            stream_response(response)
            st.session_state.materials_generated += 1
            st.session_state.messages.append({"role": "assistant", "content": response})
