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
        ["teacher", "student"],
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
    
    # Greeting responses
    if any(word in prompt_lower for word in ["hello", "hi", "hey", "start"]):
        if role == "teacher":
            return f"""👋 **Welcome, Teacher!**

I'm your CBC Lesson Material Generator. I can help you create:

📝 **Worksheets** - Practice exercises with solutions
📋 **Lesson Plans** - Structured 40-minute lessons
🎯 **Activities** - Engaging hands-on learning
✅ **Assessments** - Quizzes, tests, and rubrics

**Current Settings:**
- Grade: {grade}
- Subject: {subject}
- Material: {MATERIAL_TYPES[material_type]}

What would you like me to create today?"""
        else:
            return f"""👋 **Hello, Student!**

I can help you with:

📖 Study materials for {subject}
📝 Practice worksheets
🎯 Learning activities
💡 Topic explanations

What topic are you studying in {grade}?"""
    
    # Worksheet generation
    if material_type == "worksheet" or "worksheet" in prompt_lower:
        topic = prompt_lower.replace("worksheet", "").replace("create", "").replace("generate", "").strip()
        if not topic or len(topic) < 3:
            topic = "the current topic"
        
        return f"""# 📝 {subject} Worksheet - {grade}
### Topic: {topic.title()}

---

## **Part A: Understanding the Concept** (10 marks)

**Instructions:** Answer the following questions in the spaces provided.

1. Define or explain what {topic} means in your own words.
   
   ____________________________________________________________
   
   ____________________________________________________________

2. Give TWO real-life examples where you can observe or use {topic}.
   
   a) ____________________________________________________________
   
   b) ____________________________________________________________

3. Why is understanding {topic} important? Write one reason.
   
   ____________________________________________________________

---

## **Part B: Practice Problems** (20 marks)

**Instructions:** Solve the following problems. Show your working.

**Question 1:** [Context-based problem related to {topic}]

_Working space:_




**Question 2:** [Progressive difficulty problem]

_Working space:_




**Question 3:** [Application problem using local context]

_Working space:_




---

## **Part C: Challenge Section** (10 marks)

**Critical Thinking:** 

1. How would you explain {topic} to a younger student? Write a simple explanation.

____________________________________________________________

____________________________________________________________

2. Create your own problem about {topic} using things from your environment.

____________________________________________________________

____________________________________________________________

---

## **Teacher's Notes:**

✅ **Learning Outcomes:** Students will be able to:
- Understand the concept of {topic}
- Apply knowledge to solve problems
- Make connections to real-life situations

📊 **Assessment Criteria:**
- Understanding: 10 marks
- Problem-solving: 20 marks  
- Critical thinking: 10 marks
- **Total: 40 marks**

🎯 **Differentiation:**
- Support struggling learners with Part A
- Challenge advanced learners with Part C
- Use group work for collaborative learning

---

*Generated for {grade} - {subject} | CBC Aligned*
"""
    
    # Lesson plan generation
    elif material_type == "lesson_plan" or "lesson plan" in prompt_lower:
        topic = prompt_lower.replace("lesson plan", "").replace("create", "").replace("write", "").strip()
        if not topic or len(topic) < 3:
            topic = "today's topic"
        
        return f"""# 📋 LESSON PLAN
## {subject} - {grade}

---

### **Topic:** {topic.title()}
**Date:** ________________  
**Duration:** 40 minutes  
**Class Size:** _______

---

## **1. LEARNING OUTCOMES** 🎯

By the end of the lesson, learners should be able to:
- [ ] Explain the concept of {topic}
- [ ] Apply knowledge to solve related problems
- [ ] Demonstrate understanding through practical activities
- [ ] Work collaboratively with peers

**Specific Competencies Addressed:**
- Communication and collaboration
- Critical thinking and problem-solving
- Learning to learn

---

## **2. LEARNING RESOURCES** 📚

**Materials Needed:**
- Textbooks/reference materials
- Writing materials (pens, pencils, exercise books)
- Manila papers/chart papers
- [Specific materials for {topic}]
- Locally available resources (e.g., stones, sticks, bottle tops)

**Prerequisite Knowledge:**
Students should have prior knowledge of [related foundational concepts]

---

## **3. LESSON STRUCTURE** ⏰

### **Introduction (5 minutes)**
- Greet learners and settle the class
- Recap previous lesson briefly
- Introduce today's topic: {topic}
- Ask thought-provoking question: "Have you ever wondered about...?"
- State learning objectives clearly

### **Lesson Development (25 minutes)**

**Activity 1: Teacher Explanation (8 minutes)**
- Explain the concept of {topic} using simple language
- Use examples from learners' environment
- Draw diagrams or illustrations on the board
- Ask questions to check understanding

**Activity 2: Guided Practice (10 minutes)**
- Demonstrate a problem/activity related to {topic}
- Guide learners through solving similar problems
- Move around the class to assist individuals
- Encourage peer teaching

**Activity 3: Group Activity (7 minutes)**
- Divide class into groups of 4-5
- Give each group a task related to {topic}
- Provide materials for hands-on activity
- Monitor group progress and participation

### **Conclusion (10 minutes)**
- Groups present their findings (2-3 groups)
- Summarize key points of the lesson
- Link back to learning objectives
- Give homework/assignment
- Preview next lesson

---

## **4. ASSESSMENT METHODS** ✅

**Formative Assessment:**
- Observation during group work
- Oral questions throughout the lesson
- Quick quiz at the end

**Questions to Ask:**
1. What have we learned about {topic}?
2. Can someone give an example from our environment?
3. How can we apply this in our daily lives?

**Homework Assignment:**
[Related practice exercise or project]

---

## **5. DIFFERENTIATION STRATEGIES** 🎨

**For Struggling Learners:**
- Provide additional visual aids
- Pair with peer tutor
- Give simpler problems
- Offer more time

**For Advanced Learners:**
- Assign extension activities
- Give leadership roles in groups
- Provide challenging problems
- Encourage independent research

---

## **6. REFLECTION** 💭

**After the lesson, reflect on:**
- Were learning outcomes achieved?
- Which activities worked well?
- What needs improvement?
- Did all learners participate?
- Time management effectiveness

**Notes:**
_____________________________________________________________

_____________________________________________________________

---

*Prepared for {grade} - {subject} | CBC Aligned*
*This lesson plan follows the Competency-Based Curriculum framework*
"""
    
    # Learning activity generation
    elif material_type == "activity" or "activity" in prompt_lower:
        topic = prompt_lower.replace("activity", "").replace("create", "").replace("design", "").strip()
        if not topic or len(topic) < 3:
            topic = "the current topic"
        
        return f"""# 🎯 LEARNING ACTIVITY
## {subject} - {grade}

---

### **Activity Title:** Exploring {topic.title()}
**Duration:** 30-40 minutes  
**Group Size:** 4-5 learners per group

---

## **LEARNING OBJECTIVES** 🎓

Learners will:
1. Actively engage with concepts related to {topic}
2. Collaborate with peers to solve problems
3. Apply critical thinking skills
4. Demonstrate understanding through hands-on work

---

## **MATERIALS NEEDED** 📦

- Manila paper or chart paper (1 per group)
- Markers/crayons/colored pencils
- Exercise books for recording
- [Specific items for {topic} - use local materials]
- Examples: bottle tops, stones, seeds, sticks, newspapers

---

## **ACTIVITY INSTRUCTIONS** 📝

### **Step 1: Introduction (5 minutes)**
- Teacher explains the activity objectives
- Demonstrate what students will do
- Divide class into groups
- Assign roles: Leader, Recorder, Presenter, Materials Manager

### **Step 2: Main Activity (20-25 minutes)**

**Task for Groups:**

Your group will explore {topic} by:

1. **Discuss** (5 minutes)
   - What do you know about {topic}?
   - Share ideas within your group
   - Write down key points

2. **Create/Experiment** (10-15 minutes)
   - Use the materials provided
   - Design a model/chart/experiment about {topic}
   - Work together - everyone contributes!
   - Record your observations

3. **Prepare Presentation** (5 minutes)
   - Organize your findings
   - Choose who will present
   - Practice explaining your work

### **Step 3: Presentations (10 minutes)**
- Each group presents (2-3 minutes per group)
- Other groups ask questions
- Teacher provides feedback

---

## **GUIDING QUESTIONS** ❓

Help your group think about:
- What did you discover about {topic}?
- How does this relate to our daily lives?
- What challenges did you face?
- What would you do differently?
- How can you use this knowledge?

---

## **ASSESSMENT CRITERIA** ✅

Groups will be assessed on:

| Criteria | Points |
|----------|--------|
| Participation of all members | 5 |
| Understanding of {topic} | 5 |
| Creativity and effort | 5 |
| Presentation quality | 5 |
| **Total** | **20** |

---

## **EXTENSION ACTIVITIES** 🌟

**For Fast Finishers:**
- Research more about {topic} using library books
- Create a poster to display in class
- Teach the concept to another student

**Home Connection:**
- Find examples of {topic} at home
- Discuss with family members
- Bring an item related to {topic} for next class

---

## **TEACHER NOTES** 📌

**Preparation:**
- Collect all materials before the lesson
- Arrange classroom for group work
- Prepare sample to show students

**During Activity:**
- Circulate and observe all groups
- Ask probing questions
- Assist struggling groups
- Take photos for documentation

**Safety Considerations:**
- [List any safety rules relevant to the activity]

**Differentiation:**
- Provide extra support to groups that need it
- Give more complex tasks to advanced learners
- Allow different ways of presenting

---

*Activity designed for {grade} - {subject} | CBC Aligned*
*Promotes hands-on learning and collaboration*
"""
    
    # Assessment/Quiz generation
    elif material_type == "assessment" or material_type == "quiz" or any(word in prompt_lower for word in ["test", "exam", "quiz", "assessment"]):
        topic = prompt_lower.replace("test", "").replace("quiz", "").replace("exam", "").replace("assessment", "").strip()
        if not topic or len(topic) < 3:
            topic = "term assessment"
        
        return f"""# ✅ ASSESSMENT TOOL
## {subject} - {grade}
### {topic.title()}

---

**Name:** ______________________________  **Date:** ______________

**Class:** ________  **Time Allowed:** 60 minutes

**Total Marks:** 50

---

## **INSTRUCTIONS** 📋

1. Answer ALL questions in the spaces provided
2. Write your name and class clearly
3. Show all your working
4. Check your answers before submitting
5. Write neatly and legibly

---

## **SECTION A: Multiple Choice** (10 marks)

Choose the correct answer and write the letter in the brackets.

1. Which of the following best describes {topic}?
   - A) Option one
   - B) Option two  
   - C) Option three
   - D) Option four
   
   Answer: [ ]

2. [Question about {topic}]
   - A) 
   - B)
   - C)
   - D)
   
   Answer: [ ]

3-10. [Continue with similar format]

---

## **SECTION B: Short Answer Questions** (15 marks)

Answer the following questions briefly.

1. Define {topic} in your own words. (3 marks)

   ____________________________________________________________
   
   ____________________________________________________________
   
   ____________________________________________________________

2. Give THREE examples of {topic} from your environment. (3 marks)
   
   a) ____________________________________________________________
   
   b) ____________________________________________________________
   
   c) ____________________________________________________________

3. Explain why {topic} is important in our daily lives. (4 marks)

   ____________________________________________________________
   
   ____________________________________________________________
   
   ____________________________________________________________
   
   ____________________________________________________________

4. List TWO ways you can apply knowledge of {topic}. (2 marks)

   a) ____________________________________________________________
   
   b) ____________________________________________________________

5. What challenges might you face when dealing with {topic}? (3 marks)

   ____________________________________________________________
   
   ____________________________________________________________

---

## **SECTION C: Problem Solving** (15 marks)

Solve the following problems. Show ALL your working clearly.

**Question 1:** (5 marks)

[Context-based problem related to {topic}]

_Working:_





_Answer:_ ______________________

**Question 2:** (5 marks)

[Application problem using real-life scenario]

_Working:_





_Answer:_ ______________________

**Question 3:** (5 marks)

[Complex problem requiring critical thinking]

_Working:_





_Answer:_ ______________________

---

## **SECTION D: Extended Response** (10 marks)

**Question:** Write a short paragraph explaining {topic}. Include:
- What it is
- Why it matters
- How it's used
- An example from your life

Write at least 5-7 sentences.

____________________________________________________________

____________________________________________________________

____________________________________________________________

____________________________________________________________

____________________________________________________________

____________________________________________________________

____________________________________________________________

____________________________________________________________

---

## **MARKING SCHEME** (For Teacher Use)

| Section | Marks | Student Score |
|---------|-------|---------------|
| Section A: Multiple Choice | 10 | |
| Section B: Short Answer | 15 | |
| Section C: Problem Solving | 15 | |
| Section D: Extended Response | 10 | |
| **TOTAL** | **50** | |

**Grading Scale:**
- 45-50: Exceeds Expectations
- 35-44: Meets Expectations  
- 25-34: Approaches Expectations
- Below 25: Needs Support

**Teacher Comments:**

____________________________________________________________

____________________________________________________________

---

*Assessment for {grade} - {subject} | CBC Aligned*
*Covers knowledge, skills, and competencies*
"""
    
    # Flashcards generation
    elif material_type == "flashcards" or "flashcard" in prompt_lower:
        topic = prompt_lower.replace("flashcard", "").replace("create", "").strip()
        if not topic or len(topic) < 3:
            topic = "key concepts"
        
        return f"""# 🎴 FLASHCARDS SET
## {subject} - {grade}
### Topic: {topic.title()}

---

**Instructions for Teachers:**
1. Print these flashcards on cardstock
2. Cut along the dotted lines
3. Fold in half (question on front, answer on back)
4. Laminate for durability (optional)

**Ways to Use:**
- Individual study/revision
- Pair work (students quiz each other)
- Group games (quiz competitions)
- Quick formative assessment

---

## 📇 FLASHCARD 1
**FRONT (Question):**
> What is {topic}?

**BACK (Answer):**
> [Clear, concise definition with example]

---

## 📇 FLASHCARD 2
**FRONT (Question):**
> Give an example of {topic} from your daily life.

**BACK (Answer):**
> [Real-world example relevant to Kenyan context]

---

## 📇 FLASHCARD 3
**FRONT (Question):**
> Why is {topic} important?

**BACK (Answer):**
> [2-3 reasons explaining significance]

---

## 📇 FLASHCARD 4
**FRONT (Question):**
> How do you [action related to {topic}]?

**BACK (Answer):**
> [Step-by-step process or method]

---

## 📇 FLASHCARD 5
**FRONT (Question):**
> What tools or materials do you need for {topic}?

**BACK (Answer):**
> [List of relevant materials/tools]

---

## 📇 FLASHCARD 6
**FRONT (Question):**
> Name TWO types or categories of {topic}.

**BACK (Answer):**
> 1. [Type one with brief description]
> 2. [Type two with brief description]

---

## 📇 FLASHCARD 7
**FRONT (Question):**
> What is the difference between [A] and [B] in {topic}?

**BACK (Answer):**
> [Clear comparison highlighting key differences]

---

## 📇 FLASHCARD 8
**FRONT (Question):**
> Draw or describe [visual element related to {topic}]

**BACK (Answer):**
> [Description of expected drawing/diagram with labels]

---

## 📇 FLASHCARD 9
**FRONT (Question):**
> True or False: [Statement about {topic}]

**BACK (Answer):**
> [True/False with explanation why]

---

## 📇 FLASHCARD 10
**FRONT (Question):**
> Challenge: How can you apply {topic} to solve a problem in your community?

**BACK (Answer):**
> [Creative application showing higher-order thinking]

---

**BONUS ACTIVITY IDEAS:**

🎯 **Memory Game:** Use two sets of flashcards. Place face down. Students find matching pairs.

🏆 **Quiz Competition:** Divide class into teams. Teams earn points for correct answers.

✏️ **Create Your Own:** Students make their own flashcards about {topic}.

⏱️ **Speed Round:** How many can you answer in 2 minutes?

---

*Flashcards for {grade} - {subject} | Set of 10 cards*
*Print, cut, and laminate for classroom use*
"""
    
    # General help and guidance
    elif "help" in prompt_lower or "how" in prompt_lower:
        if role == "teacher":
            return f"""# 💡 How to Use the CBC Lesson Generator

I can create various learning materials for {grade} {subject}:

## **Available Material Types:**

### 📝 **Worksheets**
Practice exercises with problems to solve. Great for homework or classwork.
*Example: "Create a math worksheet on fractions for grade 4"*

### 📋 **Lesson Plans**
Complete 40-minute lesson plans following CBC format.
*Example: "Write a lesson plan on photosynthesis"*

### 🎯 **Learning Activities**
Hands-on group activities and experiments.
*Example: "Design a science experiment about plants"*

### ✅ **Assessments**
Tests, quizzes, and evaluation tools with marking schemes.
*Example: "Generate an end-of-term test for science"*

### 🎴 **Flashcards**
Study cards for revision and quick practice.
*Example: "Make flashcards for Kiswahili vocabulary"*

### 📖 **Study Notes**
Summaries and revision materials for students.
*Example: "Create study notes on Kenyan history"*

---

## **Tips for Best Results:**

1. **Be Specific:** Mention the exact topic you want
   - ✅ "Create worksheet on adding fractions"
   - ❌ "Create math worksheet"

2. **Mention Grade Level:** (Already set in sidebar)
   - Current: {grade}

3. **Include Context:** Tell me about your students' needs
   - "My students struggle with word problems"
   - "I need visual aids for this topic"

4. **Request Customization:**
   - "Make it culturally relevant to Kenya"
   - "Include local examples"
   - "Add illustrations"

---

## **Sample Requests:**

- "Create a worksheet on multiplication with Kenyan currency examples"
- "Write a lesson plan about clean water with hands-on activities"
- "Generate flashcards for English grammar - present tense"
- "Make an assessment tool for science - states of matter"
- "Design a group activity about healthy eating using local foods"

---

**What would you like me to create?**
"""
        else:
            return f"""# 💡 How I Can Help You Learn

Hi! I can help you study {subject} for {grade}. Here's what I can do:

## **I Can Create:**

📖 **Study Notes** - Summaries to help you understand topics better

📝 **Practice Worksheets** - Problems to practice what you've learned

🎴 **Flashcards** - Cards to help you memorize important facts

💡 **Explanations** - Break down difficult concepts into simple terms

---

## **Just Tell Me:**

1. What topic you're studying
2. What you need help with
3. What you find difficult

**Examples:**
- "I need help understanding fractions"
- "Can you explain photosynthesis simply?"
- "Make practice problems for multiplication"

---

What subject are you studying today?
"""
    
    # Default response with guidance
    else:
        material_name = MATERIAL_TYPES[material_type]
        return f"""I'll help you create {material_name} for **{grade} {subject}**.

To generate the best material, please tell me:

1. **Specific Topic:** What concept or subject area?
   - Example: "Fractions", "Photosynthesis", "Kenyan Independence"

2. **Focus Area:** What should the material emphasize?
   - Example: "Word problems", "Practical experiments", "Critical thinking"

3. **Special Requirements:** (Optional)
   - Difficulty level adjustments
   - Cultural context (Kenyan examples)
   - Specific learning outcomes
   - Visual aids needed

**Quick Example:**
*"Create a worksheet on adding fractions with word problems using Kenyan currency examples"*

What would you like me to create?"""

# --- 7. TYPING ANIMATION ---
def stream_response(response_text):
    """Creates a typing animation effect for responses."""
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
    st.markdown(f'<span
