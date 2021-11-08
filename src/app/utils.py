from decouple import config
from minio import Minio


def get_storage_client() -> Minio:
    return Minio(
        endpoint=config("MINIO_ADDRESS", default="localhost:9000"),
        access_key=config("MINIO_ACCESS_KEY"),
        secret_key=config("MINIO_SECRET_KEY"),
    )
