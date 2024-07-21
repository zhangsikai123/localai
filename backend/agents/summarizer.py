import concurrent.futures
import os
import pathlib

from agents.models.chatgpt import chatgpt_four
from agents.spliter.chinese import ChineseRecursiveTextSplitter
from langchain.chains import LLMChain
from langchain.document_loaders import TextLoader
from langchain.prompts import PromptTemplate


def process_split(idx, split, doc_path, save_results):
    page_content = split.page_content
    summary = None

    if save_results:
        os.makedirs("tmp", exist_ok=True)
        summary_path = os.path.join(
            "tmp", f"{pathlib.Path(doc_path).stem}_summary_{idx}"
        )
        if os.path.exists(summary_path):
            with open(summary_path, "r") as f:
                summary = f.read()
        else:
            summary = simple_summarize(page_content)
            with open(summary_path, "w") as f:
                f.write(summary)
    else:
        summary = simple_summarize(page_content)

    return (idx, summary)


def parallel_summarize(splits, doc_path, save_results):
    summaries = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_summary = {
            executor.submit(process_split, idx, split, doc_path, save_results): (
                idx,
                split,
            )
            for idx, split in enumerate(splits)
        }
        for future in concurrent.futures.as_completed(future_to_summary):
            idx, split = future_to_summary[future]
            try:
                summaries[idx] = future.result()[1]
            except Exception as exc:
                print("parallel_summarize an exception: %s" % (exc))

    return summaries


def simple_summarize(
    content,
):
    size_limit = 4000
    # print(f"content length: {len(content)}")
    assert len(content) < size_limit
    prompt_template = "用精简的语言重写下面这段内容。要求：1.尽量保持行文风格 2.不要超过200字: {content}"
    llm_chain = LLMChain(
        llm=chatgpt_four, prompt=PromptTemplate.from_template(prompt_template)
    )

    return llm_chain(inputs={"content": content})["text"]


def aggregate_summarize(summaries):
    prompt_template = "用精简的语言概述下面这段文字。要求：1.不超过300字 2.保持行文风格: {content}"
    llm_chain = LLMChain(
        llm=chatgpt_four, prompt=PromptTemplate.from_template(prompt_template)
    )
    return llm_chain(inputs={"content": summaries})["text"]


def word_count(doc_path):
    return len(open(doc_path).read())


def text_doc_summarize(
    doc_path=None,
    kfile=None,
    zh_title_enhance: bool = False,
    chunk_size: int = 1000,
    chunk_overlap: int = 0,
    save_results: bool = False,
    parallel: bool = False,
    refresh: bool = False,
):
    if doc_path:
        loader = TextLoader(doc_path)
        splitter = ChineseRecursiveTextSplitter(chunk_size=3000, chunk_overlap=0)
        splits = loader.load_and_split(splitter)
    elif kfile:
        doc_path = kfile.filepath
        splits = kfile.file2text(
            zh_title_enhance,
            refresh,
            chunk_size,
            chunk_overlap,
        )

    section_num = len(splits)
    assert section_num < 20
    summaries = {}
    if parallel:
        summaries = parallel_summarize(splits, doc_path, save_results)
    else:
        for i, split in enumerate(splits):
            page_content = split.page_content

            if save_results:
                os.makedirs("tmp", exist_ok=True)
                summary_path = os.path.join(
                    "tmp", f"{pathlib.Path(doc_path).stem}_summary_{i}"
                )
                if os.path.exists(summary_path):
                    with open(summary_path, "r") as f:
                        summary = f.read()
                else:
                    summary = simple_summarize(page_content)
                    with open(summary_path, "w") as f:
                        f.write(summary)
            else:
                summary = simple_summarize(page_content)
            summaries[i] = summary

    # sorted summaries values by key
    sorted_summaries = [
        v for k, v in sorted(summaries.items(), key=lambda item: item[0])
    ]
    if save_results:
        summary_path = os.path.join("tmp", f"{pathlib.Path(doc_path).stem}_summary")
        if os.path.exists(summary_path):
            all_summary = open(summary_path, "r").read()
        else:
            all_summary = aggregate_summarize("".join(sorted_summaries))
    else:
        all_summary = aggregate_summarize("".join(sorted_summaries))

    if save_results:
        with open(
            os.path.join("tmp", f"{pathlib.Path(doc_path).stem}_summary"), "w"
        ) as f:
            f.write(all_summary)
    return {"all": all_summary, "sections": sorted_summaries}
