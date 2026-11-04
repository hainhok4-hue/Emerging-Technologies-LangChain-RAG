"""Tu dong tao lai index khi PDF hoac thong so cau hinh thay doi."""
import json
from pathlib import Path

from config import CHUNK_OVERLAP, CHUNK_SIZE, EMBEDDING_MODEL, INDEX_DIR, PDF_DIR
from .pdf_reader import list_pdfs, load_pdfs
from .text_chunker import split_documents
from .vector_store import build_vector_store, load_vector_store, make_embeddings, save_vector_store


def pdf_signature(pdf_dir: Path = PDF_DIR) -> list[dict]:
    """Input: thu muc PDF. Output: thong tin file de nhan biet thay doi."""
    return [
        {'name': p.name, 'size': p.stat().st_size, 'mtime_ns': p.stat().st_mtime_ns}
        for p in list_pdfs(pdf_dir)
    ]


def build_manifest(pdf_dir: Path = PDF_DIR) -> dict:
    """Input: thu muc PDF. Output: metadata cua index va tham so."""
    return {
        'pdfs': pdf_signature(pdf_dir),
        'chunk_size': CHUNK_SIZE,
        'chunk_overlap': CHUNK_OVERLAP,
        'embedding_model': EMBEDDING_MODEL,
    }


def prepare_store(pdf_dir: Path = PDF_DIR, index_dir: Path = INDEX_DIR):
    """Input: thu muc PDF/index. Output: tuple(FAISS, created_new, num_pages, num_chunks)."""
    current = build_manifest(pdf_dir)
    if not current['pdfs']:
        raise FileNotFoundError(f'Chua co PDF trong thu muc: {pdf_dir}')
    manifest_path = index_dir / 'manifest.json'
    is_cached = False
    if manifest_path.exists():
        try:
            is_cached = (json.loads(manifest_path.read_text(encoding='utf-8')) == current
                         and (index_dir / 'index.faiss').exists()
                         and (index_dir / 'index.pkl').exists())
        except (OSError, ValueError):
            pass
    embeddings = make_embeddings(EMBEDDING_MODEL)
    if is_cached:
        print('[INFO] PDF khong doi - su dung index FAISS da luu.')
        try:
            return load_vector_store(index_dir, embeddings), False, None, None
        except Exception as exc:
            print(f'[WARN] Index cu khong doc duoc ({exc}). Dang tao moi...')
    pages = load_pdfs(pdf_dir)
    chunks = split_documents(pages, CHUNK_SIZE, CHUNK_OVERLAP)
    print(f'[INFO] Da doc {len(pages)} trang co chu, tao {len(chunks)} chunks.')
    store = build_vector_store(chunks, embeddings)
    save_vector_store(store, index_dir)
    manifest_path.write_text(json.dumps(current, ensure_ascii=False, indent=2), encoding='utf-8')
    return store, True, len(pages), len(chunks)
