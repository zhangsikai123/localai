from configs.model_config import TEMPERATURE
from langchain.prompts.chat import ChatPromptTemplate
from langchain.prompts.chat import HumanMessagePromptTemplate
from server.chat.models import model_provider

model = model_provider(
    provider_name="OpenAI", temperature=TEMPERATURE, max_tokens=50, callbacks=None
)


human_prompt = "{input}"
human_message_template = HumanMessagePromptTemplate.from_template(human_prompt)

chat_prompt = ChatPromptTemplate.from_messages(
    [("human", "Say Bob"), ("ai", "hello Bob"), ("human", "{input}")]
)


output = chat_prompt | model
print(output.invoke(input="Say Alice").content)
