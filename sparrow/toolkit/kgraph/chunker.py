# from semantic_text_splitter import TextSplitter

# def semantic_split(text: str, limit: int) -> list[str]:
#     splitter = TextSplitter(limit)
#     return splitter.chunks(text)

from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List

def chunk(text: str, chunk_size: int=1000, chunk_overlap: int=200) -> list[str]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    docs: List[Document] = text_splitter.create_documents([text])
    return [doc.page_content for doc in docs if doc.page_content.strip() != ""]  # Filter out empty chunks    

