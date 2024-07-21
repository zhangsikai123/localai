from configs.model_config import LLM_MODEL
from configs.model_config import TEMPERATURE
from langchain.prompts.chat import ChatPromptTemplate
from langchain.prompts.chat import HumanMessagePromptTemplate
from server.chat.models import model_provider
from server.utils import get_ChatOpenAI

model = model_provider(model_name=LLM_MODEL, temperature=TEMPERATURE)


human_prompt = "{input}"
human_message_template = HumanMessagePromptTemplate.from_template(human_prompt)

chat_prompt = ChatPromptTemplate.from_messages(
    [("human", "我们来玩成语接龙，我先来，生龙活虎"), ("ai", "虎头虎脑"), ("human", "{input}")]
)


output = chat_prompt | model
print(output.to_json())
