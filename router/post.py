from fastapi import *
from fastapi.responses import JSONResponse
from model.post import upload_to_s3
from database import db_pool
import logging, os

post_router = APIRouter()

AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")

@post_router.post("/api/upload")
async def get_data_from_s3(file: UploadFile = File(...)): 
  if not file or file.filename == "":
    return JSONResponse(content={"error": "No file uploaded"}, status_code=400)
  original_url = upload_to_s3(file)
  new_url = original_url.replace("booktrend-images.s3.amazonaws.com", "d2lmlyo01d222h.cloudfront.net")
  print(new_url)
  if new_url:
    return {"url": new_url}
  return JSONResponse(content={"error": "Failed to upload to S3"}, status_code=500)

@post_router.post("/api/submit")
async def save_data_from_user(content: str = Form(...), imageUrl: str = Form(...)): 
  query = "INSERT INTO posts (content, image_url) VALUES (%s, %s)"
  db_pool.get_cursor(query, (content, imageUrl))
  data = {
    'content': content,
    'image_url': imageUrl
  }
  return {"data": data}


@post_router.get("/api/posts")
async def get_all_posts():
  try:
    query = "SELECT content, image_url FROM posts ORDER BY time DESC"
    data = db_pool.get_cursor(query, fetch=True)
    return {"data": data}
  except Exception as e:
    logging.exception("資料庫查詢失敗")
    raise HTTPException(status_code=500, detail="Internal Server Error")