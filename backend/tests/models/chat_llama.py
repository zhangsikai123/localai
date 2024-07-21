from configs.model_config import TEMPERATURE
from langchain.prompts.chat import ChatPromptTemplate
from langchain.prompts.chat import HumanMessagePromptTemplate
from langchain_community.llms import Ollama

model_cls = Ollama
model_args = dict(
    temperature=TEMPERATURE,
    model="llama3",
)
model = model_cls(**model_args)

chat_prompt = ChatPromptTemplate.from_messages(
    [("human", "Say Bob"), ("ai", "hello Bob"), ("human", "{input}")]
)


output = chat_prompt | model
print(output.invoke(input="Say Alice").content)
