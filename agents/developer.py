from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser

llm = Ollama(model="gemma:2b")
output_parser = StrOutputParser()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a software developer. Generate code in a requested framework."),
    ("human", "Design: {input}")
])

def develop_code(design):
    return (prompt | llm | output_parser).invoke({"input": design})
