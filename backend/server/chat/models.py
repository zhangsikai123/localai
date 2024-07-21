import os

from langchain_community.llms import Ollama
from langchain_core.language_models.llms import BaseLLM
from langchain_openai import ChatOpenAI


def model_provider(
    model_name,
    temperature,
    max_tokens,
    callbacks,
) -> BaseLLM:
    
    if model_name == "OpenAI":
        model_cls = ChatOpenAI
        model_args = dict(
            streaming=True,
            verbose=True,
            callbacks=callbacks,
            temperature=temperature,
            max_tokens=max_tokens,
            model_name="gpt-3.5-turbo",
            openai_api_base="https://api.openai.com/v1",
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            openai_proxy=os.getenv("OPENAI_PROXY", "http://127.0.0.1:1088"),
        )
    elif model_name == "Llama":
        model_cls = Ollama
        model_args = dict(
            temperature=temperature,
            model="llama3",
        )
    else:
        raise ValueError(f"model_name: {model_name} not supported")
    return model_cls(**model_args)
