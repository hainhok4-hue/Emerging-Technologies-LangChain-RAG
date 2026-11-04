# Emerging Technologies — LLM Applications with LangChain

**Round 1 / Lần 1 — PDF Question Answering with Retrieval-Augmented Generation (RAG)**  
Python 3.11 · LangChain · FAISS · Ollama · Qwen2.5 3B · Multilingual MiniLM

> Đây là bộ mã nguồn và minh chứng thực nghiệm dành cho nhóm học phần Emerging Technologies. Đề tài triển khai ứng dụng hỏi đáp PDF, **không huấn luyện lại LLM**.

## 1. Demo hoạt động như thế nào?

```text
Offline / Indexing (khi tài liệu hoặc cấu hình thay đổi):
PDF(s) -> PyPDFLoader -> Documents -> Text Splitter -> Embeddings -> FAISS

Online / Question answering:
Question -> FAISS Retriever (top-k) -> PDF context ->
ChatPromptTemplate | ChatOllama (Qwen2.5) | StrOutputParser -> Answer
                                -> file/page/chunk + elapsed time + JSONL log
```

**Các giá trị mặc định trong `config.py`:** `chunk_size=900` ký tự, `chunk_overlap=150` ký tự, `top_k=4`, `LLM_MODEL=qwen2.5:3b`, embedding `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`.

## 2. Cách chạy demo trên Windows 11

Cài Python **3.11 (64-bit)** và [Ollama](https://ollama.com/download/windows), giải nén hoặc clone project. Trong **PowerShell** tại thư mục chứa `app.py`:

```powershell
.\01_CAI_DAT_LAN_DAU.bat
.\02_CHAY_HOI_DAP.bat
```

Đợi chương trình hiện **`BAN HOI >`**, sau đó nhập câu hỏi tiếng Việt. Ví dụ:

- `Câu lạc bộ Sách Sao Mai được thành lập năm nào?` → Dữ liệu mẫu: **2024**.
- `Câu lạc bộ sinh hoạt vào thứ mấy và lúc mấy giờ?` → Dữ liệu mẫu: **thứ Bảy, 08:00–10:00**.
- `Tổng thống Mỹ là ai?` → **Không có trong PDF mẫu**, model nên từ chối.

Gõ `exit` để thoát. Hướng dẫn chi tiết: [`docs/HUONG_DAN_GOC_CHI_TIET.md`](docs/HUONG_DAN_GOC_CHI_TIET.md).

**Lưu ý trên Windows:** `config.py` lưu chỉ mục FAISS tại `Path.home() / 'RAG_FAISS' / 'index'` nhằm tránh lỗi ghi file đã gặp với đường dẫn OneDrive chứa Unicode. Thư mục index này không có sẵn trên GitHub; ứng dụng **tự tạo lại** khi chạy.

## 3. Tập tin quan trọng

| Vị trí | Nội dung |
|---|---|
| [`app.py`](app.py), [`config.py`](config.py), [`src/`](src/) | Chương trình hỏi đáp và mã nguồn |
| [`data/pdfs/`](data/pdfs/) | PDF mẫu 3 trang dùng cho thử nghiệm |
| [`notebooks/DEMO_TUNG_HAM_DA_CHAY.ipynb`](notebooks/DEMO_TUNG_HAM_DA_CHAY.ipynb) | Notebook đã chạy có output (đã che đường dẫn máy cá nhân) |
| [`ket_qua/ket_qua_5_cau_hinh.csv`](ket_qua/ket_qua_5_cau_hinh.csv) | Thực nghiệm 5 cấu hình A–E |
| [`ket_qua/pytest_ket_qua.txt`](ket_qua/pytest_ket_qua.txt) | Pytest: 3 passed, 1 deprecation warning |
| [`tai_lieu/`](tai_lieu/) | Lưu đồ, mô tả thuật toán, 17 Function/Method, tình huống và trắc nghiệm |
| [`presentation/`](presentation/) | PowerPoint 40 trang và 11 trang phụ tùy chọn |
| [`docs/GITHUB_UPLOAD_GUIDE_VI.md`](docs/GITHUB_UPLOAD_GUIDE_VI.md) | Hướng dẫn chia sẻ và quản lý GitHub cho nhóm |

### Thực nghiệm / kiểm thử

```powershell
.\05_CHAY_NOTEBOOK_VA_LUU_KET_QUA.bat
.\06_KIEM_TRA_HO_SO_LAN1.bat
```

Bằng chứng ghi nhận ngày **04/11/2026** trên máy Windows 11 của nhóm: notebook 17 ô code có kết quả, bảng 5 cấu hình A–E, 3/3 bài test đạt. **Thí nghiệm A–E chỉ sử dụng một PDF ngắn và một câu hỏi đo; không chứng minh cấu hình nào tối ưu trong mọi trường hợp hoặc độ chính xác tổng quát.** Kết quả LLM vẫn cần đối chiếu với PDF, ngay cả khi có danh sách nguồn.

## 4. Phân công thuyết trình (40 slide)

| Thành viên | Slide | Nội dung |
|---|---|---|
| Trần Việt Hải | 1–4 | Mở đầu, giới thiệu bài toán |
| Lâm Xê Khoa | 5–15 | Nền tảng LLM, RAG, kiến trúc |
| Mai Tuấn Dũng | 16–26 | Chia chunks, Embeddings, FAISS, LCEL, lưu đồ |
| Sơn Nguyên | 27–37 | Cách chạy, đánh giá và giới hạn |
| Châu Ngọc Đức | 38 | Mở chương trình và giới thiệu demo |
| Trần Việt Hải | 39–40 | Demo câu hỏi ngoài PDF, Q&A và kết thúc |

**Canva của nhóm:** [Bản slide Lần 1](https://www.canva.com/d/QC5Mo2kRAcUVBhD). Quyền xem/chỉnh sửa tùy thuộc cài đặt chia sẻ của Canva.

## 5. Phạm vi, an toàn và giới hạn

- Dự án hiện hỗ trợ **PDF chứa văn bản**, chưa có OCR cho PDF scan ảnh.
- Không xem các đoạn truy xuất là bằng chứng tuyệt đối cho nội dung AI trả lời.
- **Không tải** `index.pkl` từ người lạ; `FAISS.load_local(..., allow_dangerous_deserialization=True)` chỉ được dùng với index đáng tin cậy.
- Không đưa `.venv/`, mô hình tải về, cache, thông tin đăng nhập hoặc lịch sử hỏi đáp cá nhân lên GitHub.
- Output notebook chia sẻ trong repository đã **ẩn đường dẫn máy tính cá nhân** mà không đổi số liệu thí nghiệm.
- Dùng repository **Private** và mời đúng thành viên; không gửi quyền chỉnh sửa công khai nếu chưa cần.
