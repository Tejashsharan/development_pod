from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser

llm = Ollama(model="gemma:2b")
output_parser = StrOutputParser()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a business analyst. Convert requirements into clear user stories."),
    ("human", "Requirements: {input}")
])

def analyze_requirements(input_text):
    return (prompt | llm | output_parser).invoke({"input": input_text})
