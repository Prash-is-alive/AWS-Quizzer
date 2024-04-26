import streamlit as st
import google.generativeai as genai
import json

# Replace with your actual API key
API_KEY = "AIzaSyAOL4UFytPMpv7FTXl2CHyTubznP2eSj1s" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

@st.cache_resource
def generate_mcq_questions(paragraph):
    prompt = f"""i will provide you a PARAGRAPH and based on that paragraph i want you to generate 10 MCQ questions. each question will have 4 options out of which only one will be correct and others will be wrong. the output should be in the format:
    [
        {{
            "question": "your question here",
            "options": ["option_1", "Option_2", "Option_3", "Option_4"],
            "correct_answer": "Option_3"
        }}
    ]PARAGRAPH: {paragraph}"""
    response = model.generate_content(prompt)
    return json.loads(response.text)

@st.cache_resource
def generate_fill_in_the_blank_questions(paragraph):
    prompt = f"""i will provide you a PARAGRAPH and based on that paragraph i want you to generate 10 fill in the blanks type questions. the output should be in the format:
    [
        {{
            "question": "your question with a blank space to fill",
            "correct_answer": "the word to fill in the blank space"
        }}
    ]PARAGRAPH: {paragraph}"""
    response = model.generate_content(prompt)
    return json.loads(response.text)

def main():
    st.title("AWS QUIZZER")
    
    # Create a text area for paragraph input
    paragraph = st.text_area("Enter your text here:", value="", height=200)
    
    # Tabs for question type selection
    tab1, tab2 = st.tabs(["Multiple Choice", "Fill in the Blanks"])

    if len(paragraph) > 0:
        with tab1:
            st.write("Answer the following MCQ questions:")
            score = 0
            quiz_questions = generate_mcq_questions(paragraph)
            
            # Display MCQ questions and options
            for i, question_data in enumerate(quiz_questions, start=1):
                selected_option = st.radio(f"**Question {i}:** {question_data['question']}", options=question_data['options'], index=None)
                if selected_option is not None:
                    if selected_option == question_data['correct_answer']:
                        score += 1

            if st.button("Submit", key="submit_mcq"):
                  st.markdown(f"<h2 style='text-align: center; color: green;'>Your score is: {score}/{len(quiz_questions)}</h2>", unsafe_allow_html=True)
        with tab2:
            st.write("Fill in the blanks:")
            score = 0
            quiz_questions = generate_fill_in_the_blank_questions(paragraph)
            
            # Display Fill in the Blanks questions and input boxes
            for i, question_data in enumerate(quiz_questions, start=1):
                answer = st.text_input(f"**Question {i}:** {question_data['question']}")
                if answer.strip().lower() == question_data['correct_answer'].lower():
                    score += 1

            if st.button("Submit", key="submit_fib"):
                st.markdown(f"<h2 style='text-align: center; color: green;'>Your score is: {score}/{len(quiz_questions)}</h2>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()