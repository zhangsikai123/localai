from configs.model_config import LLM_MODEL
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


human_prompt = "{input}"
human_message_template = HumanMessagePromptTemplate.from_template(human_prompt)

chat_prompt = ChatPromptTemplate.from_messages(
    [("human", "我们来玩成语接龙，我先来，生龙活虎"), ("ai", "虎头虎脑"), ("human", "{input}")]
)


output = chat_prompt | model
print(output.to_json())

