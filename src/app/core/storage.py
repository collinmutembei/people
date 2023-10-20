from abc import ABC, abstractmethod
from copy import deepcopy
from dataclasses import dataclass
from typing import Optional
from uuid import UUID

import magic
import pandas
from decouple import config
from minio import Minio
from starlette.datastructures import UploadFile

from app.settings.base import AppEnv, app_config


@dataclass
class UploadedData:
    filename: str
    data: pandas.DataFrame


class FileStorage(ABC):
    """Abstract factory for file storage"""

    def __init__(self):
        self.client = self.get_client()

    @abstractmethod
    def get_client(self):
        """Returns file storage client"""
        raise NotImplementedError

    @abstractmethod
    def upload_file(
        self, uploader_uuid: UUID, file_upload: UploadFile
    ) -> Optional[UploadedData]:
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
        """Creates bucket to store file when it does not exist"""
        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)

    def _get_file_type(self, file):
        """Returns the mimetype of file"""
        return magic.from_buffer(file.read(2048), mime=True)

    def upload_file(
        self, uploader_uuid: UUID, file_upload: UploadFile
    ) -> Optional[UploadedData]:
        self._prepare_bucket(self.FILE_UPLOAD_BUCKET_NAME)
        # Using deepcopy to ensure that the file.read operation
        # in _get_file_type does not close the file before upload
        filetype = self._get_file_type(deepcopy(file_upload.file))
        if filetype == "application/csv":
            uploaded_file = self.client.put_object(
                bucket_name=self.FILE_UPLOAD_BUCKET_NAME,
                object_name=f"{uploader_uuid.hex}/{file_upload.filename}",
                data=deepcopy(file_upload.file),
                length=-1,
                part_size=5 * 1024 * 1024,
                content_type=filetype,
            )
            file_data = pandas.read_csv(file_upload.file)
            return UploadedData(filename=uploaded_file.object_name, data=file_data)
        return None
