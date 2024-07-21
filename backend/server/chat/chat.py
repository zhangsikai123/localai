import asyncio

from typing import AsyncIterable
from typing import List

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
    query: str = Body(..., description="用户输入", examples=["恼羞成怒"]),
    history: List[History] = Body(
        [],
        description="历史对话",
        examples=[
            [
                {"role": "user", "content": "我们来玩成语接龙，我先来，生龙活虎"},
                {"role": "assistant", "content": "虎头虎脑"},
            ]
        ],
    ),
    stream: bool = Body(False, description="流式输出"),
    model_name: str = Body(LLM_MODEL, description="LLM 模型名称。"),
    temperature: float = Body(TEMPERATURE, description="LLM 采样温度", ge=0.0, le=1.0),
    max_tokens: int = Body(None, description="限制LLM生成Token数量，默认None代表模型最大值"),
    # top_p: float = Body(TOP_P, description="LLM 核采样。勿与temperature同时设置", gt=0.0, lt=1.0),
    prompt_name: str = Body(
        "default", description="使用的prompt模板名称(在configs/prompt_config.py中配置)"
    ),
):
    history = [History.from_data(h) for h in history]

    async def chat_iterator(
        query: str,
        history: List[History] = [],
        model_name: str = LLM_MODEL,
        prompt_name: str = prompt_name,
    ) -> AsyncIterable[str]:
        callback = AsyncIteratorCallbackHandler()
        model = models.model_provider(
            model_name=model_name,
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
        if model_name == "OpenAI":
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
            query=query, history=history, model_name=model_name, prompt_name=prompt_name
        ),
        media_type="text/event-stream",
    )
