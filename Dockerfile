# 使用官方 Python 基礎映像來運行 FastAPI
FROM python:3.9-slim

# 設定工作目錄
WORKDIR /app

# 複製需求文件並安裝依賴
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 複製程式碼和 static 前端資料夾到容器中
COPY . .

# 啟動 FastAPI
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "3000"]
