# 1. Mô tả bài toán, thuật toán và thư viện

## 1.1. Bài toán

Người dùng có một hoặc nhiều tài liệu **PDF chứa lớp văn bản**. Họ muốn nhập câu hỏi tiếng Việt vào cửa sổ CMD, nhận được câu trả lời dựa trên nội dung PDF và biết câu trả lời đã sử dụng những đoạn nào. Mục tiêu học tập là **xây dựng một ứng dụng Retrieval-Augmented Generation (RAG) bằng LangChain**, không nhằm huấn luyện một mô hình AI mới.

**Input:** một hay nhiều file `.pdf` tại `data/pdfs/` và một câu hỏi dạng chuỗi. **Output:** văn bản trả lời, danh sách tên file/trang/chunk đã truy xuất, thời gian đáp ứng, lịch sử JSONL. **Giới hạn:** không hỗ trợ PDF scan thiếu lớp văn bản; model có thể trả lời sai nên phải kiểm chứng với nguồn.

## 1.2. Mô tả giải thuật

**Giai đoạn A – lập chỉ mục (offline / khi PDF thay đổi):**

1. `list_pdfs()` tìm các file PDF trong thư mục.
2. `load_pdfs()` dùng `PyPDFLoader` đọc PDF thành `Document`, một Document mỗi trang có chữ; metadata chứa tên file/trang.
3. `split_documents()` chia Document thành những đoạn tối đa ~900 ký tự, chồng lấp 150 ký tự.
4. `make_embeddings()` lấy mô hình đa ngôn ngữ và `build_vector_store()` tạo vector cho các đoạn.
5. `save_vector_store()` lưu chỉ mục FAISS cục bộ; `build_manifest()` lưu metadata để phát hiện khi nào cần xây lại.

**Giai đoạn B – hỏi đáp (online / mỗi câu hỏi):**

1. `retrieve_documents(store, question, k)` lấy tối đa k đoạn văn tương đồng trong FAISS.
2. `format_context()` chèn tên file/trang và số thứ tự vào các đoạn.
3. `generate_answer()` kết hợp prompt + context với `ChatOllama` (`qwen2.5:3b`) qua LangChain Expression Language (LCEL).
4. `answer_question()` trả về `{answer, sources, retrieved_count}`; `app.main()` in và `save_history()` lưu log.

## 1.3. Thư viện và mục đích

| Thư viện | Class / Function dùng | Vai trò cụ thể |
|---|---|---|
| `langchain-community` | `PyPDFLoader`, `FAISS` | Đọc PDF và lưu/tìm vector |
| `langchain-text-splitters` | `RecursiveCharacterTextSplitter` | Chia trang thành chunks có overlap |
| `langchain-huggingface` | `HuggingFaceEmbeddings` | Kết nối mô hình embedding Hugging Face |
| `sentence-transformers` | `paraphrase-multilingual-MiniLM-L12-v2` | Mô hình đổi văn bản đa ngôn ngữ thành vector |
| `langchain-ollama` | `ChatOllama` | Kết nối ứng dụng với Ollama local |
| `langchain-core` | `Document`, `ChatPromptTemplate`, `StrOutputParser` | Dữ liệu chuẩn, prompt, xử lý kết quả LLM |
| `faiss-cpu` | Thư viện FAISS bên dưới vectorstore | Tìm kiếm vector tương tự nhanh |
| `pypdf` | Được `PyPDFLoader` sử dụng | Trích xuất lớp văn bản trong PDF |
| Python chuẩn | `json`, `pathlib`, `urllib`, `time`, `datetime` | Đường dẫn, kiểm tra Ollama, caching, lịch sử |
| `jupyterlab` (tùy chọn) | Notebook | Chạy các bước demo từng hàm |

## 1.4. Vì sao dùng RAG?

LLM trả lời trôi chảy nhưng không tự biết nội dung PDF mới. RAG đưa các đoạn tài liệu được tìm thấy vào prompt khi trả lời, không fine-tune lại model. Việc truy xuất làm tăng khả năng trả lời bám tài liệu, nhưng **không bảo đảm luôn chính xác**.

## 1.5. Tham số

| Tham số | Giá trị mặc định | Tác dụng |
|---|---|---|
| `CHUNK_SIZE` | 900 ký tự | Độ dài phần văn bản để embedding |
| `CHUNK_OVERLAP` | 150 ký tự | Giữ nội dung liên tiếp khi tách đoạn |
| `TOP_K` | 4 | Số chunks tối đa đưa vào prompt |
| `EMBEDDING_MODEL` | `paraphrase-multilingual-MiniLM-L12-v2` | Embedding đa ngôn ngữ |
| `LLM_MODEL` | `qwen2.5:3b` | Sinh câu trả lời tiếng Việt qua Ollama |

## 1.6. Đánh giá

Kiểm tra với câu hỏi có câu trả lời trong PDF và không có câu trả lời trong PDF. Ghi nhận nguồn truy xuất có chứa bằng chứng không (retrieval), câu trả lời có trung thành với nguồn không (faithfulness) và thời gian trả lời. Không tự nhận đã chạy thử nghiệm nếu chưa mở notebook trên máy và thu thập output thực tế.
