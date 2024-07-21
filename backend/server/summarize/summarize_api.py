import hashlib

from agents import summarizer
from fastapi import File
from fastapi import Form
from fastapi import UploadFile
from server.knowledge_base.utils import KnowledgeFile
from server.utils import BaseResponse


def get_summary(
    filename: str,
    knowledge_base_name: str,
):
    kfile = KnowledgeFile(filename, knowledge_base_name)
    result = summarizer.text_doc_summarize(
        None,
        kfile,
        zh_title_enhance=False,
        chunk_size=2000,
        chunk_overlap=200,
        save_results=True,
        parallel=True,
        refresh=False,
    )
    return BaseResponse(
        code=200,
        msg="file summary",
        data={"summary": result["all"], "sections": result["sections"]},
    )


def summarize(
    file: UploadFile = File(..., description="上传文件"),
    knowledge_base_name: str = Form(..., description="知识库名称", examples=["samples"]),
) -> BaseResponse:
    # save file into summary dir and get file_path
    file_content = file.file.read()  # 读取上传文件的内容
    filename = file.filename
    kfile = KnowledgeFile(filename, knowledge_base_name)
    md5 = hashlib.md5(file_content).hexdigest()
    # name = f"{filename}_{md5}"
    # summary_dir = os.path.join("summary", name)
    # run summarizer
    result = summarizer.text_doc_summarize(
        None,
        kfile,
        zh_title_enhance=False,
        chunk_size=2000,
        chunk_overlap=200,
        save_results=True,
        parallel=True,
        refresh=False,
    )
    return BaseResponse(
        code=200,
        msg="file summary finished",
        data={"summary": result["all"], "sections": result["sections"]},
    )
