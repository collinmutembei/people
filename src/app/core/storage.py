from abc import ABC, abstractmethod
from uuid import UUID

from decouple import config
from minio import Minio
from minio.helpers import ObjectWriteResult
from starlette.datastructures import UploadFile

from app.settings.base import AppEnv, app_config


class FileStorage(ABC):
    """Abstract factory for file storage"""

    def __init__(self):
        self.client = self.get_client()

    @abstractmethod
    def get_client(self):
        """Returns file storage client"""
        raise NotImplementedError

    @abstractmethod
    def upload_file(self, uploader_uuid: UUID, file_upload: UploadFile):
        """Uploads file to file storage"""
        raise NotImplementedError


class S3FileStorage(FileStorage):

    FILE_UPLOAD_BUCKET_NAME = config("MINIO_BUCKET_NAME", default="people")

    def get_client(self) -> Minio:
        return Minio(
            endpoint=config("MINIO_ADDRESS", default="localhost:9000"),
            access_key=config("MINIO_ACCESS_KEY"),
            secret_key=config("MINIO_SECRET_KEY"),
            secure=app_config.app_env == AppEnv.PROD,
        )

    def _prepare_bucket(self, bucket_name: str):
        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)

    def upload_file(
        self, uploader_uuid: UUID, file_upload: UploadFile
    ) -> ObjectWriteResult:
        self._prepare_bucket(self.FILE_UPLOAD_BUCKET_NAME)
        uploaded_file = self.client.put_object(
            bucket_name=self.FILE_UPLOAD_BUCKET_NAME,
            object_name=f"{uploader_uuid.hex}/{file_upload.filename}",
            data=file_upload.file,
            length=-1,
            part_size=10 * 1024 * 1024,
            content_type="application/csv",
        )
        return uploaded_file
