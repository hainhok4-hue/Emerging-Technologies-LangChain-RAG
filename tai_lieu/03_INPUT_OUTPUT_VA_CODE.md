# 3. Chi tiết Input – Output và code ví dụ của từng Function/Method

**Mọi đoạn code dưới đây được lấy trực tiếp từ bộ mã nguồn mới.** Tên biến trong ví dụ giả định những bước trước đã chạy. Không phải mọi ví dụ có thể chạy riêng lẻ khi chưa tạo các đối tượng đầu vào.

## 3.1. Bảng tổng quan

| Hàm | Input | Output |
|---|---|---|
| `list_pdfs()` | folder: Path (thư mục) | list[Path] (các tệp .pdf) |
| `load_pdfs()` | folder: Path | list[Document] (mỗi trang có chữ) |
| `split_documents()` | documents, chunk_size=900, chunk_overlap=150 | list[Document] (các chunks) |
| `make_embeddings()` | model_name: str | HuggingFaceEmbeddings |
| `build_vector_store()` | documents: list[Document], embeddings | FAISS |
| `save_vector_store()` | store: FAISS, folder: Path | None (ghi file) |
| `load_vector_store()` | folder: Path, embeddings | FAISS |
| `retrieve_documents()` | store, question: str, k: int | list[Document] |
| `format_context()` | documents: list[Document] | str |
| `generate_answer()` | question: str, documents, model_name | str |
| `answer_question()` | store, question, model_name, k=4 | dict(answer, sources, retrieved_count) |
| `pdf_signature()` | pdf_dir: Path | list[dict] |
| `build_manifest()` | pdf_dir: Path | dict |
| `prepare_store()` | pdf_dir: Path, index_dir: Path | tuple(FAISS, bool, pages/None, chunks/None) |
| `check_ollama()` | model_name: str | None hoặc RuntimeError |
| `save_history()` | question: str, result: dict, elapsed: float | None (ghi file .jsonl) |
| `main()` | stdin/console | int (mã thoát) |

## 3.2. Toàn bộ code hàm và minh họa

### 1. `list_pdfs()` — `src/pdf_reader.py`

**Mục đích:** Lọc và sắp xếp tên PDF; không mở file.

**Input:** `folder: Path (thư mục)`  
**Output:** `list[Path] (các tệp .pdf)`

**Code nguyên hàm trong dự án:**

```python
def list_pdfs(folder: Path) -> list[Path]:
    """Input: thu muc. Output: danh sach tep PDF, sap xep theo ten."""
    return sorted(
        (p for p in folder.iterdir() if p.is_file() and p.suffix.lower() == '.pdf'),
        key=lambda p: p.name.lower(),
    ) if folder.exists() else []
```

**Ví dụ sử dụng:**

```python
list_pdfs(PDF_DIR)
```

### 2. `load_pdfs()` — `src/pdf_reader.py`

**Mục đích:** Dùng PyPDFLoader; loại trang trống; giữ metadata tên file và trang.

**Input:** `folder: Path`  
**Output:** `list[Document] (mỗi trang có chữ)`

**Code nguyên hàm trong dự án:**

```python
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
```

**Ví dụ sử dụng:**

```python
load_pdfs(PDF_DIR)
```

### 3. `split_documents()` — `src/text_chunker.py`

**Mục đích:** Dùng RecursiveCharacterTextSplitter; trả lỗi nếu tham số sai.

**Input:** `documents, chunk_size=900, chunk_overlap=150`  
**Output:** `list[Document] (các chunks)`

**Code nguyên hàm trong dự án:**

```python
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
```

**Ví dụ sử dụng:**

```python
split_documents(pages, 900, 150)
```

### 4. `make_embeddings()` — `src/vector_store.py`

**Mục đích:** Tải hoặc lấy từ cache mô hình mã hóa đa ngôn ngữ.

**Input:** `model_name: str`  
**Output:** `HuggingFaceEmbeddings`

**Code nguyên hàm trong dự án:**

```python
def make_embeddings(model_name: str) -> HuggingFaceEmbeddings:
    """Input: ten model HuggingFace. Output: bo ma hoa van ban thanh vector."""
    return HuggingFaceEmbeddings(model_name=model_name)
```

**Ví dụ sử dụng:**

```python
make_embeddings(EMBEDDING_MODEL)
```

### 5. `build_vector_store()` — `src/vector_store.py`

**Mục đích:** Tính vectors của chunks và lưu trong FAISS ở RAM.

**Input:** `documents: list[Document], embeddings`  
**Output:** `FAISS`

**Code nguyên hàm trong dự án:**

```python
def build_vector_store(documents: list[Document], embeddings: HuggingFaceEmbeddings) -> FAISS:
    """Input: chunks + embedding. Output: FAISS vector store trong RAM."""
    if not documents:
        raise ValueError('Khong co doan van ban de tao FAISS.')
    return FAISS.from_documents(documents, embeddings)
```

**Ví dụ sử dụng:**

```python
build_vector_store(chunks, emb)
```

### 6. `save_vector_store()` — `src/vector_store.py`

**Mục đích:** Tạo index.faiss và index.pkl; không sao chép file index.pkl từ người lạ.

**Input:** `store: FAISS, folder: Path`  
**Output:** `None (ghi file)`

**Code nguyên hàm trong dự án:**

```python
def save_vector_store(store: FAISS, folder: Path) -> None:
    """Input: FAISS + thu muc. Output: tep index.faiss va index.pkl tren o dia."""
    folder.mkdir(parents=True, exist_ok=True)
    store.save_local(str(folder))
```

**Ví dụ sử dụng:**

```python
save_vector_store(store, INDEX_DIR)
```

### 7. `load_vector_store()` — `src/vector_store.py`

**Mục đích:** Chỉ đọc index do dự án tự tạo; không mở pickle không đáng tin.

**Input:** `folder: Path, embeddings`  
**Output:** `FAISS`

**Code nguyên hàm trong dự án:**

```python
def load_vector_store(folder: Path, embeddings: HuggingFaceEmbeddings) -> FAISS:
    """Input: index da tao + embedding. Output: FAISS vector store de tim kiem.

    CANH BAO: index.pkl dung pickle; chi tai lai index tin cay do ban tao.
    Khong copy index.pkl tu nguon la vao folder nay.
    """
    if not (folder / 'index.faiss').exists() or not (folder / 'index.pkl').exists():
        raise FileNotFoundError('Chua tao index FAISS')
    return FAISS.load_local(str(folder), embeddings, allow_dangerous_deserialization=True)
```

**Ví dụ sử dụng:**

```python
load_vector_store(INDEX_DIR, emb)
```

### 8. `retrieve_documents()` — `src/qa.py`

**Mục đích:** FAISS tìm tối đa k đoạn gần với câu hỏi.

**Input:** `store, question: str, k: int`  
**Output:** `list[Document]`

**Code nguyên hàm trong dự án:**

```python
def retrieve_documents(store, question: str, k: int = 4) -> list[Document]:
    """Input: FAISS + cau hoi + top_k. Output: toi da k doan lien quan."""
    if not question.strip():
        return []
    return store.as_retriever(search_kwargs={'k': k}).invoke(question)
```

**Ví dụ sử dụng:**

```python
retrieve_documents(store, 'Câu lạc bộ họp khi nào?', 4)
```

### 9. `format_context()` — `src/qa.py`

**Mục đích:** Gắn chỉ số [1], tên file và số trang vào context.

**Input:** `documents: list[Document]`  
**Output:** `str`

**Code nguyên hàm trong dự án:**

```python
def format_context(documents: list[Document]) -> str:
    """Input: cac chunk tim duoc. Output: chuoi ngu canh co [i], ten tep, trang."""
    parts: list[str] = []
    for idx, doc in enumerate(documents, start=1):
        page_num = int(doc.metadata.get('page', 0)) + 1
        filename = doc.metadata.get('source', 'khong-ro.pdf')
        parts.append(f'[{idx}] File: {filename}; Trang: {page_num}\n{doc.page_content}')
    return '\n\n'.join(parts)
```

**Ví dụ sử dụng:**

```python
format_context(retrieved)
```

### 10. `generate_answer()` — `src/qa.py`

**Mục đích:** Prompt | ChatOllama | StrOutputParser; yêu cầu trả lời bám tài liệu.

**Input:** `question: str, documents, model_name`  
**Output:** `str`

**Code nguyên hàm trong dự án:**

```python
def generate_answer(question: str, documents: list[Document], model_name: str) -> str:
    """Input: cau hoi, chunk truy xuat, model Ollama. Output: cau tra loi String."""
    if not documents:
        return 'Toi khong tim thay thong tin nay trong PDF.'
    llm = ChatOllama(model=model_name, temperature=0)
    chain = PROMPT | llm | StrOutputParser()
    return chain.invoke({'question': question, 'context': format_context(documents)}).strip()
```

**Ví dụ sử dụng:**

```python
generate_answer('Họp lúc nào?', retrieved, LLM_MODEL)
```

### 11. `answer_question()` — `src/qa.py`

**Mục đích:** Điều phối retrieve và generate rồi trả dữ liệu cho giao diện.

**Input:** `store, question, model_name, k=4`  
**Output:** `dict(answer, sources, retrieved_count)`

**Code nguyên hàm trong dự án:**

```python
def answer_question(store, question: str, model_name: str, k: int = 4) -> dict:
    """Input: FAISS, cau hoi, model, k. Output: dict(answer, sources, retrieved_count)."""
    docs = retrieve_documents(store, question, k=k)
    answer = generate_answer(question, docs, model_name)
    sources = [
        {'file': doc.metadata.get('source', '?'),
         'page': int(doc.metadata.get('page', 0)) + 1,
         'chunk_id': doc.metadata.get('chunk_id')}
        for doc in docs
    ]
    return {'answer': answer, 'sources': sources, 'retrieved_count': len(docs)}
```

**Ví dụ sử dụng:**

```python
answer_question(store, 'Mượn được mấy cuốn?', LLM_MODEL)
```

### 12. `pdf_signature()` — `src/pipeline.py`

**Mục đích:** Lấy size + mtime_ns để phát hiện thay đổi PDF.

**Input:** `pdf_dir: Path`  
**Output:** `list[dict]`

**Code nguyên hàm trong dự án:**

```python
def pdf_signature(pdf_dir: Path = PDF_DIR) -> list[dict]:
    """Input: thu muc PDF. Output: thong tin file de nhan biet thay doi."""
    return [
        {'name': p.name, 'size': p.stat().st_size, 'mtime_ns': p.stat().st_mtime_ns}
        for p in list_pdfs(pdf_dir)
    ]
```

**Ví dụ sử dụng:**

```python
pdf_signature(PDF_DIR)
```

### 13. `build_manifest()` — `src/pipeline.py`

**Mục đích:** Đóng gói tên PDF, dấu thời gian, embedding và chunk config.

**Input:** `pdf_dir: Path`  
**Output:** `dict`

**Code nguyên hàm trong dự án:**

```python
def build_manifest(pdf_dir: Path = PDF_DIR) -> dict:
    """Input: thu muc PDF. Output: metadata cua index va tham so."""
    return {
        'pdfs': pdf_signature(pdf_dir),
        'chunk_size': CHUNK_SIZE,
        'chunk_overlap': CHUNK_OVERLAP,
        'embedding_model': EMBEDDING_MODEL,
    }
```

**Ví dụ sử dụng:**

```python
build_manifest(PDF_DIR)
```

### 14. `prepare_store()` — `src/pipeline.py`

**Mục đích:** Tự động lập chỉ mục nếu PDF đổi, không thì nạp chỉ mục đã lưu.

**Input:** `pdf_dir: Path, index_dir: Path`  
**Output:** `tuple(FAISS, bool, pages|None, chunks|None)`

**Code nguyên hàm trong dự án:**

```python
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
```

**Ví dụ sử dụng:**

```python
prepare_store(PDF_DIR, INDEX_DIR)
```

### 15. `check_ollama()` — `app.py`

**Mục đích:** Ping API /api/tags để kiểm tra Ollama và model.

**Input:** `model_name: str`  
**Output:** `None hoặc RuntimeError`

**Code nguyên hàm trong dự án:**

```python
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
```

**Ví dụ sử dụng:**

```python
check_ollama(LLM_MODEL)
```

### 16. `save_history()` — `app.py`

**Mục đích:** Lưu nhật ký câu hỏi, câu trả lời, nguồn, thời gian.

**Input:** `question: str, result: dict, elapsed: float`  
**Output:** `None (ghi file .jsonl)`

**Code nguyên hàm trong dự án:**

```python
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
```

**Ví dụ sử dụng:**

```python
save_history('Câu hỏi', result, 1.5)
```

### 17. `main()` — `app.py`

**Mục đích:** Chạy vòng lặp CLI; input, hiển thị kết quả, exit.

**Input:** `stdin/console`  
**Output:** `int (mã thoát)`

**Code nguyên hàm trong dự án:**

```python
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
```

**Ví dụ sử dụng:**

```python
python app.py
```

## 3.3. Input / Output của các method LangChain gọi trực tiếp

| Method của thư viện | Input | Output | Vị trí dùng |
|---|---|---|---|
| `PyPDFLoader(path).load()` | Đường dẫn PDF | `list[Document]` (mỗi trang) | `src/pdf_reader.py` |
| `RecursiveCharacterTextSplitter(...).split_documents(docs)` | list Document | list chunks Document | `src/text_chunker.py` |
| `FAISS.from_documents(chunks, embeddings)` | chunks + đối tượng embeddings | FAISS vector store | `src/vector_store.py` |
| `store.save_local(dir)` | thư mục đích | ghi tệp `.faiss`/`.pkl` | `src/vector_store.py` |
| `FAISS.load_local(dir, emb, ...)` | thư mục + embedding | FAISS vector store | `src/vector_store.py` |
| `store.as_retriever(search_kwargs={"k": k}).invoke(q)` | `q: str` | `list[Document]` tối đa k | `src/qa.py` |
| `PROMPT | ChatOllama(...) | StrOutputParser()` | dict `question`, `context` | câu trả lời chuỗi | `src/qa.py` |

## 3.4. Gợi ý trình bày

Khi demo, trình bày tuần tự theo các file: pdf_reader → text_chunker → vector_store → qa → pipeline → app. Với mỗi hàm, nói 3 ý: dữ liệu vào là gì, xử lý gì, dữ liệu trả ra là gì. Sau đó mở notebook để hiển thị các đối tượng Document, chunks và câu trả lời thật.