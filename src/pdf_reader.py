"""Chi doc tep .pdf co lop van ban; PDF scan anh can OCR (khong trong pham vi)."""
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


def list_pdfs(folder: Path) -> list[Path]:
    """Input: thu muc. Output: danh sach tep PDF, sap xep theo ten."""
    return sorted(
        (p for p in folder.iterdir() if p.is_file() and p.suffix.lower() == '.pdf'),
        key=lambda p: p.name.lower(),
    ) if folder.exists() else []


def load_pdfs(folder: Path) -> list[Document]:
    """Input: thu muc chua PDF. Output: trang co van ban duoi dang Document."""
    pdfs = list_pdfs(folder)
    if not pdfs:
        raise FileNotFoundError(f'Chua co file PDF trong: {folder}')

    documents: list[Document] = []
    for pdf in pdfs:
        try:
            pages = PyPDFLoader(str(pdf)).load()
        except Exception as exc:
            raise RuntimeError(f'Khong doc duoc PDF {pdf.name}: {exc}') from exc
        for page in pages:
            if page.page_content and page.page_content.strip():
                # 'page' tu PyPDFLoader bat dau bang 0 (trang thu 1 -> 0).
                page.metadata['source'] = pdf.name
                documents.append(page)
    if not documents:
        raise ValueError('PDF khong trich xuat duoc chu. Neu la ban scan anh, can OCR.')
    return documents
