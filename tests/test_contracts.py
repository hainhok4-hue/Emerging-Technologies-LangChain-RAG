"""Kiem tra tinh nhat quan ve tham so va mau du lieu (can cai requirements)."""
import sys
from pathlib import Path

import pytest
from langchain_core.documents import Document

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.pdf_reader import list_pdfs
from src.text_chunker import split_documents
from src.qa import format_context


def test_pdf_only(tmp_path):
    (tmp_path / 'abc.pdf').touch()
    (tmp_path / 'doc.txt').touch()
    assert [p.name for p in list_pdfs(tmp_path)] == ['abc.pdf']


def test_chunk_validation():
    with pytest.raises(ValueError):
        split_documents([Document(page_content='text')], chunk_size=100, chunk_overlap=100)


def test_context_page_number():
    doc = Document(page_content='Lich hop thu Bay', metadata={'source':'demo.pdf','page':0})
    assert 'Trang: 1' in format_context([doc])
