import uuid, os, boto3
from botocore.exceptions import ClientError

AWS_S3_KEY = os.getenv("AWS_S3_KEY")
AWS_S3_SECRET = os.getenv("AWS_S3_SECRET")
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")

s3 = boto3.client(
  "s3",
  aws_access_key_id=AWS_S3_KEY,
  aws_secret_access_key=AWS_S3_SECRET,
)

def upload_to_s3(file_obj, bucket_name=AWS_S3_BUCKET, object_name=None):
  if not object_name:
    object_name = f"uploads/{uuid.uuid4()}_{file_obj.filename}"
  try:
    s3.upload_fileobj(file_obj.file, bucket_name, object_name)
    url = f"https://d2lmlyo01d222h.cloudfront.net/{object_name}"
    return url
  except ClientError as e:
    print("Upload failed:", e)
    return None
