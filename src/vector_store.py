"""Tao/load chi muc FAISS. Chi nap index do chinh chuong trinh tao."""
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings


def make_embeddings(model_name: str) -> HuggingFaceEmbeddings:
    """Input: ten model HuggingFace. Output: bo ma hoa van ban thanh vector."""
    return HuggingFaceEmbeddings(model_name=model_name)


def build_vector_store(documents: list[Document], embeddings: HuggingFaceEmbeddings) -> FAISS:
    """Input: chunks + embedding. Output: FAISS vector store trong RAM."""
    if not documents:
        raise ValueError('Khong co doan van ban de tao FAISS.')
    return FAISS.from_documents(documents, embeddings)


def save_vector_store(store: FAISS, folder: Path) -> None:
    """Input: FAISS + thu muc. Output: tep index.faiss va index.pkl tren o dia."""
    folder.mkdir(parents=True, exist_ok=True)
    store.save_local(str(folder))


def load_vector_store(folder: Path, embeddings: HuggingFaceEmbeddings) -> FAISS:
    """Input: index da tao + embedding. Output: FAISS vector store de tim kiem.

    CANH BAO: index.pkl dung pickle; chi tai lai index tin cay do ban tao.
    Khong copy index.pkl tu nguon la vao folder nay.
    """
    if not (folder / 'index.faiss').exists() or not (folder / 'index.pkl').exists():
        raise FileNotFoundError('Chua tao index FAISS')
    return FAISS.load_local(str(folder), embeddings, allow_dangerous_deserialization=True)
