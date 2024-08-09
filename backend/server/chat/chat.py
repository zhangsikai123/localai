import asyncio

from typing import AsyncIterable
from typing import List
from configs import MAX_TOKEN
from configs import LLM_MODEL
from configs import TEMPERATURE
from fastapi import Body
from fastapi.responses import StreamingResponse
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.prompts.chat import ChatPromptTemplate
from server.chat import models
from server.chat.utils import History
from server.utils import get_prompt_template
from server.utils import wrap_done


async def chat(
    query: str = Body(..., description="user input", examples=["恼羞成怒"]),
    history: List[History] = Body(
        [],
        description="history chat",
        examples=[
            [
                {"role": "user", "content": "我们来玩成语接龙，我先来，生龙活虎"},
                {"role": "assistant", "content": "虎头虎脑"},
            ]
        ],
    ),
    stream: bool = Body(False, description="streaming response"),
    provider_name: str = Body(LLM_MODEL, description="LLM provider"),
    temperature: float = Body(TEMPERATURE, description="LLM temperature", ge=0.0, le=1.0),
    max_tokens: int = Body(MAX_TOKEN, description="token limit"),
    # top_p: float = Body(TOP_P, description="LLM core sampling. Dont set with temperature", gt=0.0, lt=1.0),
    prompt_name: str = Body(
        "default", description="prompt name(configs/prompt_config.py)"
    ),
):
    history = [History.from_data(h) for h in history]

    async def chat_iterator(
        query: str,
        history: List[History] = [],
        provider_name: str = LLM_MODEL,
        prompt_name: str = prompt_name,
    ) -> AsyncIterable[str]:
        callback = AsyncIteratorCallbackHandler()
        model = models.model_provider(
            provider_name=provider_name,
            temperature=temperature,
            max_tokens=max_tokens,
            callbacks=[callback],
        )
        prompt_template = get_prompt_template("llm_chat", prompt_name)
        input_msg = History(role="user", content=prompt_template).to_msg_template(False)
        chat_prompt = ChatPromptTemplate.from_messages(
            [i.to_msg_template() for i in history] + [input_msg]
        )
        chain = chat_prompt | model
        # Begin a task that runs in the background.
        if provider_name == "OpenAI":
            task = asyncio.create_task(
                wrap_done(chain.ainvoke({"input": query}), callback.done),
            )
            async for token in callback.aiter():
                # Use server-sent-events to stream the response
                yield token

            await task
        else:
            async for chunks in chain.astream(query):
                for chunk in chunks:
                    yield chunk

    return StreamingResponse(
        chat_iterator(
            query=query, history=history, provider_name=provider_name, prompt_name=prompt_name
        ),
        media_type="text/event-stream",
    )
