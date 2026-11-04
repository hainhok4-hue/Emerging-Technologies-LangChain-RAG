"""Chia PDF theo doan bang LangChain RecursiveCharacterTextSplitter."""
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(
    documents: list[Document], chunk_size: int = 900, chunk_overlap: int = 150
) -> list[Document]:
    """Input: documents + do dai/overlap. Output: danh sach chunk Document."""
    if chunk_size <= 0:
        raise ValueError('chunk_size phai lon hon 0')
    if not (0 <= chunk_overlap < chunk_size):
        raise ValueError('chunk_overlap phai tu 0 den nho hon chunk_size')
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=['\n\n', '\n', '. ', ' ', ''],
    )
    chunks = splitter.split_documents(documents)
    for idx, doc in enumerate(chunks, start=1):
        doc.metadata['chunk_id'] = idx
    return chunks
