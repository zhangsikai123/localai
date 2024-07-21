import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_ROOT_PATH = ".models"
MODEL_PATH = {
    "embed_model": {
        "text-embedding-ada-002": OPENAI_API_KEY,
    },
    "llm_model": {
        "chatglm-6b": "THUDM/chatglm-6b",
    },
}

ONLINE_LLM_MODEL = {
    "baichuan-api": {
        "version": "Baichuan2-53B",  # 当前支持 "Baichuan2-53B"， 见官方文档。
        "api_key": "",
        "secret_key": "",
        "provider": "BaiChuanWorker",
    },
}

LANGCHAIN_LLM_MODEL = {
    "OpenAI": {
        "model_name": "gpt-3.5-turbo",
        "api_base_url": "https://api.openai.com/v1",
        "api_key": OPENAI_API_KEY,
        "openai_proxy": "http://127.0.0.1:1088",
    }
}

EMBEDDING_MODEL = "text-embedding-ada-002"  # 可以尝试最新的嵌入式sota模型：bge-large-zh-v1.5


# Embedding 模型运行设备。设为"auto"会自动检测，也可手动设定为"cuda","mps","cpu"其中之一。
EMBEDDING_DEVICE = "auto"

# LLM 名称
LLM_MODEL = "Llama"

# LLM 运行设备。设为"auto"会自动检测，也可手动设定为"cuda","mps","cpu"其中之一。
LLM_DEVICE = "auto"

# 历史对话轮数
HISTORY_LEN = 3

# LLM通用对话参数
TEMPERATURE = 0.7
# TOP_P = 0.95 # ChatOpenAI暂不支持该参数


# nltk 模型存储路径
NLTK_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "nltk_data")


VLLM_MODEL_DICT = {
    "aquila-7b": "BAAI/Aquila-7B",
}
