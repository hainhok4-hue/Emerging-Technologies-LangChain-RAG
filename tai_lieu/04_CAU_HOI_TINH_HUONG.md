# 4. Bộ câu hỏi tình huống cho các nhóm (kèm hướng trả lời)

1. **Nếu tài liệu là PDF scan bằng ảnh, chương trình có trả lời được không?** Không chắc; PyPDFLoader cần lớp văn bản. Phải OCR hoặc chuẩn bị PDF có thể bôi đen chữ.
2. **Tại sao cùng câu hỏi nhưng đáp án đôi lúc khác nhau?** LLM sinh ngôn ngữ có tính xác suất; cấu hình model/prompt/chunks có ảnh hưởng. `temperature=0` giảm nhưng không loại bỏ sự khác nhau.
3. **Nếu PDF rất dài thì vì sao cần chia chunks?** Hạn chế kích thước context và giúp tìm những đoạn liên quan thay vì đưa toàn bộ PDF.
4. **Nếu chunk_size quá nhỏ thì sao?** Thông tin bị chia vụn, thiếu ngữ cảnh, retrieval có thể kém.
5. **Nếu chunk_overlap bằng 0 thì sao?** Nội dung tại ranh giới các đoạn dễ bị đứt mạch.
6. **Nếu chunk_overlap lớn bằng chunk_size thì sao?** Tham số không hợp lệ; hàm `split_documents()` ném `ValueError`.
7. **Nếu tăng TOP_K từ 2 lên 8 thì điều gì đổi?** Thêm context, tăng chi phí/ngữ cảnh và nguy cơ nhiễu; không nhất thiết tốt hơn.
8. **Đổi file PDF nhưng quên tạo lại index có sao không?** Hệ thống có manifest tự phát hiện file thay đổi khi khởi động lại và tự tạo index mới.
9. **Vì sao dùng mô hình embedding đa ngôn ngữ?** Vì PDF/câu hỏi có thể bằng tiếng Việt.
10. **Nếu không mở Ollama thì sao?** `check_ollama()` dừng với hướng dẫn chạy Ollama trước khi tạo câu trả lời.
11. **Nguồn truy xuất có đồng nghĩa câu trả lời chính xác không?** Không. Vẫn phải kiểm chứng câu trả lời với PDF.
12. **Nếu người dùng hỏi thông tin không có trong PDF?** Prompt yêu cầu model báo không tìm thấy; đây là hướng dẫn, không phải bảo đảm tuyệt đối.
13. **FAISS có phải cơ sở dữ liệu SQL không?** Không; đây là chỉ mục vector dùng tìm kiếm tương đồng.
14. **Nếu nguồn PDF chứa lệnh “bỏ qua hướng dẫn”, phải làm gì?** Xem văn bản PDF là dữ liệu không tin cậy, không tuân lệnh nằm trong PDF.
15. **Vì sao không được tải index.pkl từ nguồn lạ?** Python pickle có thể thực thi mã độc khi giải tuần tự; chỉ tải index tự tạo và kiểm soát.

**Gợi ý giao cho các nhóm khác:** Cho họ chạy lần lượt 2 câu có thông tin, 1 câu ngoài PDF, 1 trường hợp thử thay PDF, 1 cấu hình chunk_size mới; yêu cầu ghi nhận nguồn và giải thích kết quả, không chỉ đánh giá “trả lời hay”.
