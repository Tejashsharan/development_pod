from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser

llm = Ollama(model="gemma:2b")
output_parser = StrOutputParser()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a QA tester. Generate test cases, run them, and provide pass score and feedback."),
    ("human", "Code:\n{input}")
])

def test_code(code):
    return (prompt | llm | output_parser).invoke({"input": code})
