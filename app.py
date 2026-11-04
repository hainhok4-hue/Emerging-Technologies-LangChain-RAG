"""Chay tu CHAY_HOI_DAP.bat hoac: python app.py."""
import json
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime

from config import INDEX_DIR, LLM_MODEL, OLLAMA_URL, PDF_DIR, RESULTS_DIR, TOP_K
from src.pdf_reader import list_pdfs
from src.pipeline import prepare_store
from src.qa import answer_question


def check_ollama(model_name: str = LLM_MODEL) -> None:
    """Input: model name. Output: None; raise RuntimeError neu Ollama chua san sang."""
    try:
        with urllib.request.urlopen(f'{OLLAMA_URL}/api/tags', timeout=4) as response:
            info = json.load(response)
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        raise RuntimeError(
            'Khong ket noi duoc Ollama. Hay mo ung dung Ollama tren Windows; '
            'neu can, mo CMD khac va chay: ollama serve'
        ) from exc
    names = [m.get('name', '') for m in info.get('models', [])]
    if model_name not in names:
        raise RuntimeError(
            f'Chua co model {model_name}. Mo CMD va chay: ollama pull {model_name}'
        )


def save_history(question: str, result: dict, elapsed: float) -> None:
    """Input: cau hoi, cau tra loi, thoi gian. Output: them 1 dong JSONL vao ket_qua."""
    RESULTS_DIR.mkdir(exist_ok=True, parents=True)
    record = {
        'timestamp': datetime.now().isoformat(timespec='seconds'),
        'question': question,
        'answer': result['answer'],
        'sources': result['sources'],
        'elapsed_seconds': round(elapsed, 2),
    }
    with (RESULTS_DIR / 'lich_su_hoi_dap.jsonl').open('a', encoding='utf-8') as stream:
        stream.write(json.dumps(record, ensure_ascii=False) + '\n')


def main() -> int:
    """Input: ban phim. Output: in cau tra loi + nguon; 0 neu thoat binh thuong."""
    print('=' * 67)
    print('         DEMO HOI DAP PDF - LANGCHAIN + RAG + OLLAMA')
    print('=' * 67)
    pdfs = list_pdfs(PDF_DIR)
    if not pdfs:
        print(f'[LOI] Hay copy it nhat 1 file .pdf vao: {PDF_DIR}')
        return 1
    print('PDF tim thay: ' + ', '.join(p.name for p in pdfs))
    try:
        check_ollama()
        store, created, pages, chunks = prepare_store()
        print(f'[OK] FAISS: {"vua tao moi" if created else "da tai lai"}.')
        print('Nhap cau hoi bang tieng Viet; nhap exit de thoat.')
        while True:
            try:
                question = input('\nBAN HOI > ').strip()
            except (EOFError, KeyboardInterrupt):
                print('\nKet thuc demo.')
                return 0
            if question.lower() in ('exit', 'quit', 'q', 'thoat'):
                print('Da thoat.')
                return 0
            if not question:
                print('Hay nhap mot cau hoi.')
                continue
            t0 = time.perf_counter()
            try:
                result = answer_question(store, question, LLM_MODEL, TOP_K)
            except Exception as exc:
                print(f'[LOI] Khong the tao cau tra loi: {exc}')
                print('Kiem tra Ollama dang chay va may du RAM.')
                continue
            elapsed = time.perf_counter() - t0
            print('\nTRA LOI:\n' + result['answer'])
            print('\nCAC DOAN DA TRUY XUAT (can kiem chung voi PDF):')
            for source in result['sources']:
                print(f" - {source['file']} | trang {source['page']} | chunk {source['chunk_id']}")
            print(f'Thoi gian: {elapsed:.2f} giay')
            save_history(question, result, elapsed)
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        print(f'\n[LOI] {exc}')
        return 1
    except Exception as exc:
        print(f'\n[LOI KHONG MONG DOI] {type(exc).__name__}: {exc}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
