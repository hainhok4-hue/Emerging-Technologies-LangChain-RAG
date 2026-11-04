KET QUA THUC TE - LAN 1 / ACTUAL RUN EVIDENCE

Da chay tren Windows 11 cua nhom vao ngay 04/11/2026.
- notebooks/DEMO_TUNG_HAM_DA_CHAY.ipynb: 17 code cells with actual outputs; no recorded execution errors.
- ket_qua/ket_qua_5_cau_hinh.csv: 5 measured configurations A-E (one sample question).
- ket_qua/pytest_ket_qua.txt: 3 passed, 1 warning.
- ket_qua/BAO_CAO_KIEM_TRA_LAN1.txt: offline audit checks passed.
- ket_qua/lich_su_hoi_dap.jsonl: sample interactive question/answer history.

CHU Y:
1. Time measurements apply to this machine and these test inputs only. Do not generalize accuracy or performance from one sample.
2. A retrieved source list is not proof that an answer is grounded in the cited text.
3. config.py uses Path.home()/RAG_FAISS/index to avoid Windows Unicode/OneDrive FAISS write issues observed on the demo machine. The index is built at runtime and is not included in the submission.
4. .venv, local model weights and cached FAISS index are intentionally not packaged; install dependencies and Ollama locally when rerunning.
5. Some notebook outputs contain local Windows paths/user-folder names. Review before distributing outside the class.
