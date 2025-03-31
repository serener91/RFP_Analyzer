import json

from langchain_community.document_loaders import PyPDFLoader
from PyPDF2 import PdfReader
import os
import pandas as pd
from tqdm import tqdm
import re


def extract_contents(file_path):
    loader = PyPDFLoader(file_path)
    pages = []
    for page in tqdm(loader.lazy_load(), desc="extracting pages"):
        pages.append(page)

    return pages


def extract_text(doc_pages):
    contexts = []
    for i in tqdm(range(len(doc_pages)), desc="extracting text"):
        contexts.append(doc_pages[i].page_content)

    return contexts


def extract_metadata(doc_pages):
    sources = []
    src_pages = []

    for i in tqdm(range(len(doc_pages)), desc="extracting text"):
        sources.append(os.path.basename(doc_pages[i].metadata["source"]))

        # PDF viewer page
        src_pages.append(doc_pages[i].metadata["page_label"])

    return sources, src_pages


def save_to_excel(meta_source, meta_page, meta_content):
    df = pd.DataFrame.from_dict(
        {
            "sources": meta_source,
            "pages": meta_page,
            "contexts": meta_content
        }
    )

    print(df)
    df.to_excel("./gto_proposal.xlsx", index=False)


def extract_pdf(pdf_path):
    """
    src_data = 2025년 경기관광정보서비스 통합 운영 과업지시서.pdf
    metadata_info = extract_pdf(src_data)
    print(metadata_info)

    print("Source:", os.path.basename(metadata_info["source"]))
    print("Total Pages:", metadata_info["total_pages"])
    print("Metadata:", metadata_info["metadata"])
    print("Page Number:", metadata_info["page_numbers"][10])
    print("Page Text:", metadata_info["texts"][10])
    """

    # with open(pdf_path, "rb") as file:
    reader = PdfReader(pdf_path)

    # Extract document metadata
    metadata = reader.metadata  # Returns a dictionary
    total_pages = len(reader.pages)

    # Extract page-specific metadata
    # page_metadata = []

    page_numbers = []
    texts = []
    for page_number, page in tqdm(enumerate(reader.pages, start=1), desc="extracting pages..."):
        # page_info = {
        #     "page_number": page_number,
        #     "text": page.extract_text(),
        # }
        # page_metadata.append(page_info)
        page_numbers.append(page_number)
        texts.append(page.extract_text())

    return {
        "source": pdf_path,
        "total_pages": total_pages,
        "metadata": metadata,
        "page_numbers": page_numbers,
        "texts": texts
        # "pages": page_metadata,
    }


def mar_filter(texts, text_ids):
    mar_pages = []
    mar_texts = []
    word_to_filter = "MAR"
    for txt_info in zip(texts, text_ids):
        if word_to_filter in txt_info[0]:
            mar_texts.append(txt_info[0])
            mar_pages.append(txt_info[1])
        else:
            continue

    return mar_texts, mar_pages


def sfr_filter(texts, text_ids):
    sfr_pages = []
    sfr_texts = []
    word_to_filter = "SFR"
    for txt_info in zip(texts, text_ids):
        if word_to_filter in txt_info[0]:
            sfr_texts.append(txt_info[0])
            sfr_pages.append(txt_info[1])
        else:
            continue

    return sfr_texts, sfr_pages


def budget_filter(texts, text_ids):
    page_limit = 10
    page_texts = []
    page_numbers = []
    words_to_filter = ["사업비", "사 업 비"]
    for txt_info in zip(texts[:page_limit], text_ids[:page_limit]):
        for word_to_filter in words_to_filter:
            if word_to_filter in txt_info[0]:
                page_texts.append(txt_info[0])
                page_numbers.append(txt_info[1])
            else:
                continue

    return page_texts, page_numbers


def time_filter(texts, text_ids):
    page_limit = 10
    page_texts = []
    page_numbers = []
    words_to_filter = ["사업기간", "용역기간"]
    for txt_info in zip(texts[:page_limit], text_ids[:page_limit]):
        for word_to_filter in words_to_filter:
            if word_to_filter in txt_info[0]:
                page_texts.append(txt_info[0])
                page_numbers.append(txt_info[1])
            else:
                continue

    return page_texts, page_numbers


def get_relevant_texts(data, filter_name):
    with open("./common/document_filter.json", "r", encoding="utf-8") as f:
        words_to_filter = json.load(f)[filter_name]

    metadata_info = data

    json_text = [
        json.dumps({
            # "Source": os.path.basename(metadata_info["source"]),
            "Page": metadata_info["page_numbers"][i],
            "Content": re.sub(r'-\s*\d+\s*-', '', metadata_info["texts"][i])
        }, ensure_ascii=False)
        for i in range(metadata_info["total_pages"])
    ]

    json_data = json.loads(json.dumps(json_text, ensure_ascii=False), strict=False)

    filtered_page = []
    filtered_text = ""
    for record in json_data:
        record_data = json.loads(record)
        if any(word in record_data["Content"] for word in words_to_filter):
            filtered_text += f"###{json.dumps(record_data, ensure_ascii=False)}, "
            filtered_page.append(record_data["Page"])

    return filtered_text, filtered_page


if __name__ == '__main__':
    src_data = r"C:\Users\gukhwan\OneDrive - (주)스위트케이\바탕 화면\ChatRFP\data\2. 제안요청서_다누림홈페이지.pdf"

    filter_name = "time_extractor"

    data_info = extract_pdf(src_data)
    text_info = get_relevant_texts(data_info, filter_name=filter_name)
    print(text_info)

    from langfuse import Langfuse
    from dotenv import load_dotenv

    load_dotenv(r"C:\Users\gukhwan\OneDrive - (주)스위트케이\바탕 화면\ChatRFP\monitoring\.env")


    def fetch_prompt(prompt_id, label="latest", version=None):
        """

        dev only

        """
        langfuse = Langfuse(
            host="http://localhost:3000"
        )
        if version is None:
            return langfuse.get_prompt(prompt_id, label=label).compile()

        else:
            return langfuse.get_prompt(prompt_id, version=version).compile()

    system_prompts = fetch_prompt(filter_name)

    from utils import inference
    output = inference(
        gpt=True,
        model="gpt-4o",
        system_msg=system_prompts,
        query=text_info,
        temperature=0.2
    )
    print(output)

