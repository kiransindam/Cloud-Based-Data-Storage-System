import uuid
import boto3
from botocore.exceptions import ClientError
from fastapi import UploadFile
from app.core.config import get_settings

settings = get_settings()


class StorageService:
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        self.bucket = settings.S3_BUCKET_NAME

    def _generate_key(self, user_id: int, filename: str) -> str:
        ext = filename.rsplit(".", 1)[-1] if "." in filename else "bin"
        unique = uuid.uuid4().hex
        return f"users/{user_id}/{unique}.{ext}"

    async def upload(self, user_id: int, file: UploadFile) -> dict:
        key = self._generate_key(user_id, file.filename)
        content = await file.read()
        try:
            self.s3.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=content,
                ContentType=file.content_type or "application/octet-stream",
            )
        except ClientError as e:
            raise RuntimeError(f"S3 upload failed: {e}")
        return {"s3_key": key, "size_bytes": len(content)}

    def generate_presigned_url(self, s3_key: str) -> str:
        try:
            return self.s3.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket, "Key": s3_key},
                ExpiresIn=settings.S3_PRESIGNED_URL_EXPIRY,
            )
        except ClientError as e:
            raise RuntimeError(f"Presigned URL failed: {e}")

    def delete(self, s3_key: str) -> None:
        try:
            self.s3.delete_object(Bucket=self.bucket, Key=s3_key)
        except ClientError as e:
            raise RuntimeError(f"S3 delete failed: {e}")


storage = StorageService()
