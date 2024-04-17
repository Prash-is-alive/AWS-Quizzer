import streamlit as st
import google.generativeai as genai
import json

API_KEY = "AIzaSyAOL4UFytPMpv7FTXl2CHyTubznP2eSj1s"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

@st.cache_resource
def generate_questions(paragraph):
    prompt = f"""i will provide you a PARAGRAPH and based on that paragraph i want you to generate 10 questions. each question will have 4 options out of which only one will be correct and others will be wrong. the output should be in the format:
    [
        {{
            "question": "your question here",
            "options": ["option_1", "Option_2", "Option_3", "Option_4"],
            "correct_answer": "Option_3"
        }}
    ]PARAGRAPH: {paragraph}"""
    response = model.generate_content(prompt)
    return json.loads(response.text)

def main():
    st.title("AWS QUIZZER")
    st.write("Answer the following questions:")
    
    # Create a text area for paragraph input
    paragraph = st.text_area("Enter your text here:", value="", height=200)
    
    # Generate questions and display them if paragraph is entered
    if len(paragraph) > 0:
        score = 0
        quiz_questions = generate_questions(paragraph)
        
        # Iterate through quiz questions
        for i, question_data in enumerate(quiz_questions, start=1):
            # Display options
            selected_option = st.radio(f"**Question {i}:** {question_data['question']}", options=question_data['options'], index=None)

            # Check if selected answer is correct
            if selected_option is not None:
                if selected_option == question_data['correct_answer']:
                    score += 1
        
        # Display final score when Submit button is clicked
        if st.button("Submit"):
            st.markdown(f"<h1 style='text-align: center; color: #ff5733;'>Your score is: {score}/{len(quiz_questions)}</h1>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
