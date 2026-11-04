"""Cau hinh du an: sua tai day neu muon doi model / chunk / top_k."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PDF_DIR = ROOT / 'data' / 'pdfs'
INDEX_DIR = Path.home() / 'RAG_FAISS' / 'index'
RESULTS_DIR = ROOT / 'ket_qua'

# Qwen2.5:3b duoc Ollama phat hanh va co ho tro tieng Viet.
LLM_MODEL = 'qwen2.5:3b'
# Sentence Transformers: mo hinh embedding da ngon ngu.
EMBEDDING_MODEL = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
CHUNK_SIZE = 900              # so ky tu, khong phai so token
CHUNK_OVERLAP = 150          # so ky tu lap lai
TOP_K = 4                    # so doan duoc truy xuat
OLLAMA_URL = 'http://localhost:11434'
