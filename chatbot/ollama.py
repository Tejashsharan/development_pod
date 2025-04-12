from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["LANGCHAIN_TRACING_V2"] = "true"

# LLM setup
llm = Ollama(model="gemma:2b")
output_parser = StrOutputParser()

# Session state for memory
if "last_code" not in st.session_state:
    st.session_state.last_code = ""
if "iteration" not in st.session_state:
    st.session_state.iteration = 0

# Agent prompt templates
ba_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a business analyst. Convert the following requirements into clear user stories."),
    ("human", "Requirements: {input}")
])

designer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a software designer. Create a UI/UX design strategy or description based on the given user stories."),
    ("human", "User Stories: {input}")
])

developer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a software developer. Write Python (Streamlit) code to implement the following design."),
    ("human", "Design: {input}")
])

tester_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a QA Tester. Analyze the following code, generate tests, and return a test pass percentage with feedback."),
    ("human", "Code:\n{input}")
])

# Agent chains
def run_chain(prompt, input_text):
    return (prompt | llm | output_parser).invoke({"input": input_text})

# Streamlit UI
st.title("🛠️ AI Development Pod")

input_text = st.text_area("Enter your web app requirements or request fixes:", height=150)

submit = st.button("Submit")

# Handle refinement requests
if input_text and "function" in input_text.lower() and "fix" in input_text.lower():
    st.write("🔄 Fix request detected...")
    fix_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a developer. Fix the function mentioned based on the error described."),
        ("human", "Existing Code:\n{code}\n\nFix Request:\n{fix}")
    ])
    fix_chain = fix_prompt | llm | output_parser
    fixed_code = fix_chain.invoke({
        "code": st.session_state.last_code,
        "fix": input_text
    })
    st.markdown("### 🔧 Fixed Code:")
    st.code(fixed_code, language="python")
    st.session_state.last_code = fixed_code

elif submit and input_text:
    # Step 1: BA Agent
    user_stories = run_chain(ba_prompt, input_text)
    st.markdown("### 🧠 Business Analyst Output (User Stories)")
    st.write(user_stories)

    # Step 2: Designer Agent
    design = run_chain(designer_prompt, user_stories)
    st.markdown("### 🎨 Designer Output (Design Strategy)")
    st.write(design)

    # Step 3: Developer Agent
    code = run_chain(developer_prompt, design)
    st.markdown("### 💻 Developer Output (Code)")
    st.code(code, language="python")
    st.session_state.last_code = code

    # Step 4: Tester Agent
    score_response = run_chain(tester_prompt, code)
    st.markdown("### 🧪 Tester Output")
    st.write(score_response)

    # Extract score
    import re
    score_match = re.search(r'(\d{1,3})%', score_response)
    score = int(score_match.group(1)) if score_match else 0

    if score >= 90:
        st.success("✅ Code passed testing successfully!")
    else:
        st.warning("⚠️ Code failed testing. Sending back to Developer for revision...")
        if st.session_state.iteration < 3:
            feedback_prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a developer. Revise the code based on the tester's feedback."),
                ("human", "Previous Code:\n{code}\n\nFeedback:\n{feedback}")
            ])
            revised_code = (feedback_prompt | llm | output_parser).invoke({
                "code": code,
                "feedback": score_response
            })
            st.code(revised_code, language="python")
            st.session_state.last_code = revised_code
            st.session_state.iteration += 1
        else:
            st.error("❌ Maximum retry limit reached.")

