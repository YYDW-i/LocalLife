# LocalLife（个人生活控制台）

本地优先（Local-first）、隐私友好、功能精致的个人生活管理软件。

## 开发模式启动（推荐）
### 后端
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
