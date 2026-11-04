# LANGCHAIN PDF Q&A - BỘ DEMO MỚI CHO WINDOWS 11

**Mục tiêu:** Bạn bỏ file PDF vào thư mục, mở chương trình, nhập câu hỏi bằng tiếng Việt và nhận câu trả lời dựa trên PDF đó. Chương trình sử dụng **LangChain + RAG + FAISS + Ollama**; không yêu cầu API key trả phí.

> **Chạy đơn giản nhất:** Cài Python + Ollama, nhấp đúp `01_CAI_DAT_LAN_DAU.bat` **một lần**, sau đó nhấp đúp `02_CHAY_HOI_DAP.bat` để bắt đầu hỏi đáp. ZIP có sẵn PDF mẫu để thử ngay.

## A. HƯỚNG DẪN TỪ ĐẦU (CHỈ CẦN LÀM THEO)

### Bước 1 — Cài Python và Ollama

**Hai ứng dụng cần cài trước:**

- **Python 3.11 (64-bit):** https://www.python.org/downloads/ — nên đánh dấu **Add Python to PATH** khi cài.
- **Ollama cho Windows:** https://ollama.com/download/windows — cài xong hãy mở ứng dụng **Ollama** từ Start Menu.

**Để kiểm tra:** mở CMD, nhập hai dòng sau (từng dòng một):

```bat
python --version
ollama --version
```

Nếu chưa hiện phiên bản, cài hoặc mở lại CMD/VS Code trước khi làm tiếp.

### Bước 2 — Giải nén dự án đúng cách

1. Giải nén file ZIP mới. Bạn sẽ thấy **một thư mục** tên `LangChain_PDF_QA_MOI`.
2. Mở thư mục đó; kiểm tra thấy trực tiếp các file `01_CAI_DAT_LAN_DAU.bat`, `02_CHAY_HOI_DAP.bat`, `README.md` và `app.py`.
3. Không cần mở lại dự án LangChain cũ và không cần chép đè code cũ.

### Bước 3 — Cài thư viện và tải AI (chỉ thực hiện lần đầu)

**Nhấp đúp vào file** `01_CAI_DAT_LAN_DAU.bat`.

File BAT tự động:

1. Tạo môi trường Python `.venv` cho dự án.
2. Cài thư viện theo `requirements.txt`.
3. Tải model AI `qwen2.5:3b` về Ollama (khoảng **1,9 GB**).

Chờ thông báo `[OK] DA CAI DAT XONG!`. **Lần đầu phải có Internet**. Lần đầu chạy hỏi đáp còn có thể tải thêm mô hình embedding từ Hugging Face. Tốc độ phụ thuộc máy của bạn.

### Bước 4 — Thêm file PDF của bạn

Mở thư mục:

```text
data\pdfs\
```

Trong ZIP có sẵn file `TAI_LIEU_DEMO_CAU_LAC_BO_SACH.pdf` (3 trang, nội dung giả định) để thử. Bạn có thể **xóa PDF mẫu rồi chép PDF của mình** vào thư mục này. Nếu để nhiều PDF thì chương trình tìm kiếm trong tất cả các file đó.

**Quan trọng:** PDF cần có lớp văn bản có thể bôi đen/copy. Bản scan ảnh không có OCR nên chưa được hỗ trợ trong demo đơn giản này.

### Bước 5 — Chạy để đặt câu hỏi

**Nhấp đúp vào file** `02_CHAY_HOI_DAP.bat`.

Chương trình sẽ tự động đọc PDF, chia đoạn, tạo embeddings, lập chỉ mục FAISS và hiển thị:

```text
BAN HOI >
```

Giờ bạn gõ câu hỏi rồi nhấn **Enter**. Ví dụ với PDF mẫu:

```text
BAN HOI > Câu lạc bộ Sách Sao Mai thành lập năm nào?
BAN HOI > Câu lạc bộ sinh hoạt vào thứ mấy và lúc mấy giờ?
BAN HOI > Mỗi thành viên được mượn tối đa bao nhiêu cuốn sách?
BAN HOI > Quá hạn trả sách bị xử lý ra sao?
BAN HOI > Ai là hiệu trưởng của trường? 
BAN HOI > exit
```

Đầu ra gồm **câu trả lời**, **nguồn được truy xuất (tên file, số trang, chunk)**, **thời gian xử lý**. Lịch sử tự lưu trong `ket_qua/lich_su_hoi_dap.jsonl`.

> **Từ lần thứ hai:** Chỉ mở `02_CHAY_HOI_DAP.bat`. Khi bạn thay PDF hoặc tham số chia đoạn, chương trình tự phát hiện và tạo lại chỉ mục. Khi chỉ đặt câu hỏi mới thì không cần lập chỉ mục lại.

## B. NẾU BẠN MUỐN CHẠY TRONG TERMINAL VS CODE

Chọn **Terminal → New Terminal → Command Prompt** (CMD). **Không chọn Git Bash** như lỗi bạn đã gặp trước đây. Mở terminal ngay trong thư mục chứa file BAT (có thể nhấp chuột phải vào thư mục dự án rồi mở Terminal).

**Cài đặt lần đầu:**

```bat
01_CAI_DAT_LAN_DAU.bat
```

**Chạy hỏi đáp:**

```bat
02_CHAY_HOI_DAP.bat
```

**Kiểm tra nếu bị lỗi:**

```bat
04_KIEM_TRA_MOI_TRUONG.bat
```

**Mở notebook minh họa từng hàm** (cài thêm JupyterLab nếu cần):

```bat
03_MO_NOTEBOOK.bat
```

**Không copy dấu Markdown** `` ```bat `` và `` ``` `` vào CMD; chỉ copy các dòng lệnh ở bên trong. Nếu CMD báo `'xxx.bat' is not recognized`, bạn đang ở **sai thư mục**. Cách dễ nhất là nhấp đúp trực tiếp vào `.bat` từ File Explorer.

## C. SƠ ĐỒ HOẠT ĐỘNG

```text
GIAI ĐOẠN A: CHUẨN BỊ TÀI LIỆU (khi PDF thay đổi)
PDF → PyPDFLoader → Documents theo trang → chia chunks
    → HuggingFace Embeddings → chỉ mục FAISS (lưu ở data/index)

GIAI ĐOẠN B: HỎI ĐÁP (mỗi câu hỏi)
Câu hỏi → tìm top-k chunks trong FAISS → tạo context
        → Prompt | ChatOllama (Qwen2.5) | StrOutputParser
        → trả lời + in nguồn được truy xuất + lưu lịch sử
```

Đây là **Retrieval-Augmented Generation (RAG)**: đưa đoạn tài liệu liên quan vào prompt, **không phải huấn luyện lại mô hình AI**.

## D. CÁC FILE ĐÃ SOẠN SẴN ĐỂ NỘP BÀI

| Tên file / thư mục | Chức năng |
|---|---|
| `app.py` | Giao diện CMD nhập câu hỏi / trả lời / ghi log |
| `config.py` | Đổi model, kích thước chunks, overlap, top-k |
| `src/pdf_reader.py` | Hàm tìm và đọc PDF |
| `src/text_chunker.py` | Hàm chia chunks |
| `src/vector_store.py` | Hàm embedding, tạo/lưu/nạp FAISS |
| `src/qa.py` | Tìm đoạn liên quan và gọi LLM bằng LangChain |
| `src/pipeline.py` | Tạo index / tự nạp index nếu PDF không thay đổi |
| `notebooks/DEMO_TUNG_HAM.ipynb` | Notebook ví dụ từng Method và **5 bộ tham số A–E** |
| `data/pdfs/TAI_LIEU_DEMO_CAU_LAC_BO_SACH.pdf` | PDF mẫu có thể hỏi đáp ngay |
| `data/CAU_HOI_THU_DEMO.txt` | Câu hỏi gợi ý + thông tin kiểm chứng |
| `tai_lieu/01_MO_TA_VA_THU_VIEN.md` | Mô tả bài toán, thuật toán, thư viện |
| `tai_lieu/02_LUU_DO.md` | Hai lưu đồ xử lý + các nhánh lỗi |
| `tai_lieu/03_INPUT_OUTPUT_VA_CODE.md` | Input/Output và code **17 hàm** lấy từ code thật |
| `tai_lieu/04_CAU_HOI_TINH_HUONG.md` | **15 câu hỏi tình huống** cho nhóm khác |
| `tai_lieu/15_CAU_TRAC_NGHIEM.txt` | **15 câu hỏi trắc nghiệm** và đáp án |
| `tai_lieu/LangChain_PDF_QA_40_Slides.pptx` | **PowerPoint 40 slide** theo yêu cầu |
| `tai_lieu/LUU_DO_RAG_TONG_QUAT.png` | Ảnh lưu đồ tổng quát chèn PowerPoint |

## E. DEMO CÁC BỘ THAM SỐ

Bạn có thể mở `03_MO_NOTEBOOK.bat` để chạy từng cell của `notebooks/DEMO_TUNG_HAM.ipynb`. Notebook hướng dẫn đầu vào/đầu ra từng Method, tạo embedding, FAISS, truy xuất và hỏi đáp. Cuối notebook so sánh 5 cấu hình:

| Bộ | chunk_size | overlap | top_k |
|---|---:|---:|---:|
| A | 500 | 50 | 2 |
| B | 700 | 100 | 3 |
| C | 900 | 150 | 4 |
| D | 1100 | 200 | 3 |
| E | 1300 | 250 | 5 |

Chạy xong, notebook xuất dữ liệu thật vào `ket_qua/ket_qua_5_cau_hinh.csv`. **File ZIP chưa có kết quả chạy benchmark được tạo sẵn** — bạn cần chạy notebook trên máy rồi chụp màn hình / đưa kết quả vào slide khi nộp.

Nếu chỉ muốn đổi tham số của ứng dụng, mở `config.py` và sửa:

```python
CHUNK_SIZE = 900
CHUNK_OVERLAP = 150
TOP_K = 4
LLM_MODEL = 'qwen2.5:3b'
```

**Nếu máy RAM ít** hoặc Qwen 3B quá chậm: chạy `ollama pull qwen2.5:1.5b` trong CMD, sau đó sửa `LLM_MODEL` trong `config.py` thành `qwen2.5:1.5b` rồi mở lại ứng dụng. Model nhỏ có thể trả lời kém hơn.

## F. LỖI THƯỜNG GẶP VÀ CÁCH SỬA

| Lỗi / hiện tượng | Cách sửa |
|---|---|
| `bash: ...bat: command not found` | Bạn ở Git Bash. Chuyển Terminal → Command Prompt (CMD) hoặc nhấp đúp file BAT. |
| `'01_CAI_DAT_LAN_DAU.bat' is not recognized` | Mở CMD **đúng thư mục** chứa file `.bat`. |
| `'python' is not recognized` | Cài Python 3.11, bật PATH và mở lại CMD. |
| `No module named ...` | Chạy lại `01_CAI_DAT_LAN_DAU.bat`, cần Internet lần đầu. |
| `Không kết nối được Ollama` | Mở ứng dụng Ollama; nếu cần mở CMD khác và chạy `ollama serve`. |
| `Chưa có model qwen2.5:3b` | Trong CMD chạy `ollama pull qwen2.5:3b`. |
| `Chưa có PDF` | Chép ít nhất 1 file `.pdf` vào `data/pdfs/`. |
| `PDF không trích xuất được chữ` | PDF có thể là scan ảnh; chuyển qua OCR trước. |
| Câu trả lời không liên quan | Kiểm tra PDF đúng chủ đề, nguồn truy xuất, chất lượng PDF; thử tăng TOP_K hoặc đổi chunks. |
| File PDF đã đổi nhưng app vẫn hỏi nội dung cũ | Thoát bằng `exit`, mở lại `02_CHAY_HOI_DAP.bat`; chương trình sẽ tự kiểm tra để tái lập chỉ mục. |
| Cài `faiss-cpu` lỗi | Ưu tiên Python 3.11 64-bit; thử cập nhật pip qua file BAT cài đặt. |

## G. GIỚI HẠN / BẢO MẬT / NGUỒN THAM KHẢO

- PDF có thể chứa nội dung sai. Model cũng có thể đưa ra đáp án thiếu chính xác, ngay cả khi có RAG. **Hãy đối chiếu trực tiếp các trang đã truy xuất**.
- Không đưa `data/index/index.pkl` từ người lạ vào dự án: cơ chế tải index FAISS dùng `pickle`, tiềm ẩn nguy cơ nếu file bị sửa độc hại.
- PDF của bạn không tự động gửi lên dịch vụ LLM trả phí; Ollama chạy local. Nhưng **lần đầu** cần tải mô hình embedding từ Hugging Face và model LLM từ Ollama.
- Nếu PDF chứa thông tin nhạy cảm, không chia sẻ PDF, thư mục `data/index` hoặc thư mục `ket_qua` công khai.
- Phần OCR, bảng biểu ảnh phức tạp và đánh giá tự động chất lượng ngoài phạm vi demo đơn giản này.

Tài liệu API chính thức:

- LangChain: https://docs.langchain.com/oss/python/langchain/overview
- PyPDFLoader: https://reference.langchain.com/python/langchain-community/document_loaders/pdf/PyPDFLoader
- FAISS: https://github.com/langchain-ai/langchain-community/blob/main/libs/community/langchain_community/vectorstores/faiss.py
- Ollama Qwen2.5: https://ollama.com/library/qwen2.5

**Tình trạng kiểm thử:** Mã nguồn đã được kiểm tra cú pháp, cấu trúc notebook, file PPTX và khả năng trích xuất chữ của PDF mẫu. **Chưa thể kiểm tra thực tế việc cài LangChain/Ollama và sinh câu trả lời end-to-end trên máy Windows 11 của bạn**; lần chạy đầu của bạn sẽ xác nhận phần này.
