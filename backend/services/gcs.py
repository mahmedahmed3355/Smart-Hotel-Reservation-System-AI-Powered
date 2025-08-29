# services/gcs.py
import os
from google.cloud import storage

def upload_to_gcs(local_path: str, bucket_name: str, dst_path: str) -> str:
    client = storage.Client.from_service_account_json(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(dst_path)
    blob.upload_from_filename(local_path)
    blob.make_public()  # أو خليه خاص حسب سياساتك
    return blob.public_url
