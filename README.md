This is an interactive Streamlit application designed to help teachers generate Competency-Based Curriculum (CBC) aligned educational materials. It allows users to quickly create worksheets, lesson plans, learning activities, assessment tools, flashcards, and study notes based on selected grade levels and subjects.

## ✨ Features

- **Dynamic Material Generation**: Generate various types of educational content on demand.
- **CBC Alignment**: Templates are structured to align with the Kenyan Competency-Based Curriculum.
- **Configurable Settings**: Easily select grade level, subject, and material type via a sidebar.
- **Interactive Chat Interface**: Use a chat-like input to specify topics for material generation.
- **Real-time Previews**: View generated materials directly within the application.
- **Example Prompts**: Quick buttons to generate common requests.
- **Session Management**: Maintains chat history and settings across interactions.

## 🛠️ Setup and Installation (Local)

To run this application on your local machine, follow these steps:

1.  **Clone the Repository (or copy the script)**:
    If this is part of a larger repository, clone it:
    ```bash
    git clone <repository_url>
    cd cbc-lesson-generator-app
    ```
    Otherwise, save the provided Python script (e.g., `app.py`) to your local machine.

2.  **Create a Virtual Environment (Recommended)**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install Dependencies**:
    The application primarily relies on `streamlit`.
    ```bash
    pip install streamlit
    ```

4.  **Run the Streamlit Application**:
    Navigate to the directory where you saved `app.py` and run:
    ```bash
    streamlit run app.py
    ```

    Your browser should automatically open to `http://localhost:8501` (or another port if 8501 is in use), displaying the application.

## 🚀 Usage

1.  **Configure Settings**: Use the sidebar to select the **Grade Level**, **Subject**, and **Material Type** you wish to generate.
2.  **Enter Your Request**: In the chat input box at the bottom, type your request. Be specific about the topic.
    *   Example: "Create study notes on fractions"
    *   Example: "Generate a worksheet about the water cycle"
    *   Example: "Write a lesson plan for ancient civilizations"
3.  **Generate Material**: Press Enter or click the send button. The application will generate the material based on your selections and prompt.
4.  **Review and Iterate**: The generated material will appear in the main chat area. You can adjust your settings or provide new prompts to refine the output.
5.  **Clear Chat**: Use the "Clear Chat" button in the sidebar to reset the conversation.

## 📝 Material Types Available

-   **Worksheet** (📝): Practice exercises and problems.
-   **Lesson Plan** (📋): Structured 40-minute lesson plans.
-   **Learning Activity** (🎯): Hands-on group activities and experiments.
-   **Assessment Tool** (✅): Quizzes, tests, and evaluation tools.
-   **Flashcards** (🎴): Study cards for revision.
-   **Study Notes** (📖): Summaries and revision materials.

## 🚧 Future Enhancements

-   **Download Feature**: Implement functionality to export generated materials as PDF or Word documents.
-   **Advanced Customization**: Offer more options for tailoring content (e.g., specific learning objectives, cultural context).
-   **Expanded Material Types**: Introduce project guides or other educational resources.

## 🤝 Contributing

Contributions are welcome! If you have suggestions or want to improve the application, please feel free to open issues or submit pull requests.
