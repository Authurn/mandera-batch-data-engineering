from minio import Minio
from minio.error import S3Error

client = Minio(
    "localhost:9001",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

bucket_name = "mandera-data-lake"

files_to_upload = [
    "customers_transformed.csv",
    "products_transformed.csv",
    "orders_transformed.csv"
]

for file_name in files_to_upload:
    try:
        client.fput_object(
            bucket_name,
            file_name,
            file_name
        )
        print(f"✅ Uploaded {file_name} to MinIO")

    except S3Error as e:
        print("❌ Error occurred:", e)