import os

from langchain_community.llms import Ollama
from langchain_core.language_models.llms import BaseLLM
from langchain_openai import ChatOpenAI

model_list = {
    "gpt-3.5-turbo": {"provider": "OpenAI"},
    "llama3": {"provider": "Llama"},
}


def model_provider(
    model_name,
    temperature,
    max_tokens,
    callbacks,
) -> BaseLLM:
    if model_name not in model_list:
        raise ValueError(f"model_name: {model_name} not supported")

    if model_list[model_name]["provider"] == "OpenAI":
        model_cls = ChatOpenAI
        model_args = dict(
            streaming=True,
            verbose=True,
            callbacks=callbacks,
            temperature=temperature,
            max_tokens=max_tokens,
            model_name=model_name,
            openai_api_base="https://api.openai.com/v1",
            openai_api_key=os.getenv("API_KEY"),
        )
    elif model_list[model_name]["provider"] == "Llama":
        model_cls = Ollama
        model_args = dict(
            temperature=temperature,
            model=model_name,
        )
    else:
        raise ValueError(f"model_type: {model_list[model_name]} not supported")
    return model_cls(**model_args)
