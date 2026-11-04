# Hướng dẫn đưa bài Emerging Technologies lên GitHub (không cần lệnh Git)

1. Đăng nhập GitHub bằng tài khoản cá nhân.
2. Mở **https://github.com/new**. Đặt tên `Emerging-Technologies-LangChain-RAG`, Owner là tài khoản của mình, chọn **Private**, **không tích khởi tạo README/.gitignore/license**, rồi nhấn **Create repository**.
3. Giải nén file ZIP `GITHUB_READY_Emerging_Technologies_LangChain_RAG.zip` trên Windows.
4. Trong repository GitHub mới, chọn liên kết **uploading an existing file** hoặc **Add file → Upload files**.
5. Mở thư mục đã giải nén. **Kéo toàn bộ nội dung bên trong** (không phải file `.zip` và không phải thư mục bao ngoài) vào cửa sổ Upload Files trên GitHub: README.md, .gitignore, src, docs, data, presentation... (Nếu Edge không chọn nhiều thư mục qua nút chọn file, hãy kéo-thả trực tiếp từ File Explorer.)
6. Kiểm tra ở danh sách upload có đường dẫn kiểu `src/qa.py`, `notebooks/DEMO_TUNG_HAM_DA_CHAY.ipynb`, `presentation/Emerging_Technologies_LAN1_FINAL_40_SLIDES.pptx`.
7. Ở **Commit message**, nhập `Initial submission — Emerging Technologies Round 1`, rồi nhấn **Commit changes** (hoặc nút tương đương hiện trên màn hình).
8. Về trang đầu repository: phải thấy file **README.md** và các thư mục `src`, `notebooks`, `presentation`, `ket_qua`, `tai_lieu`.
9. Mời bạn cùng nhóm: **Settings → Collaborators → Add people**, tìm GitHub username của từng người, gửi lời mời và chờ họ chấp nhận.
10. Gửi link repository và Canva vào nhóm Messenger. Các thành viên được mời mới mở được repository Private.

> Nếu muốn nhờ ChatGPT cập nhật file trực tiếp trên repository trong lần sau, mở **Settings → Plugins** của ChatGPT, kết nối GitHub và cấp quyền ứng dụng truy cập đúng repository này.

## Nhớ tránh
- Không tải nguyên file ZIP lên GitHub rồi nghĩ source sẽ tự bung ra.
- Không đăng công khai file chứa mật khẩu, khóa API, dữ liệu người dùng, `.venv`, `index.pkl`.
- Không chọn Public khi nhóm chỉ muốn chia sẻ nội bộ.
