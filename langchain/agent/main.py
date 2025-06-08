from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM



load_dotenv()
#
# llm = ChatAnthropic(
#     model="claude-2.1",
#     temperature=0,
#     max_tokens=1024,
#     timeout=None,
#     max_retries=2,
#     # other params...
# )
#
# response = llm.invoke("What are you?")

# print(response)


template = """Question: {question}

Answer: Let's think step by step."""

prompt = ChatPromptTemplate.from_template(template)

model = OllamaLLM(model="llama3.1")

chain = prompt | model

response = chain.invoke({"question": "What is LangChain?"})

print(response)



