from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser

llm = Ollama(model="gemma:2b")
output_parser = StrOutputParser()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a UI/UX designer. Generate design strategy and optionally wireframe prompts."),
    ("human", "User Stories: {input}")
])

def design_app(user_stories):
    return (prompt | llm | output_parser).invoke({"input": user_stories})
