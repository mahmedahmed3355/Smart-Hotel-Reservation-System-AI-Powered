import sys
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1]),
)

from services.gcs import upload_to_gcs


def test_upload_to_gcs_uploads_file_and_returns_public_url(monkeypatch):
    monkeypatch.setenv(
        "GOOGLE_APPLICATION_CREDENTIALS",
        "/tmp/service-account.json",
    )

    client = Mock()
    bucket = Mock()
    blob = Mock()
    blob.public_url = "https://storage.googleapis.com/test-bucket/ids/test.png"

    client.bucket.return_value = bucket
    bucket.blob.return_value = blob

    with patch(
        "services.gcs.storage.Client.from_service_account_json",
        return_value=client,
    ) as from_service_account_json:
        result = upload_to_gcs(
            "/tmp/test.png",
            "test-bucket",
            "ids/test.png",
        )

    from_service_account_json.assert_called_once_with(
        "/tmp/service-account.json"
    )
    client.bucket.assert_called_once_with("test-bucket")
    bucket.blob.assert_called_once_with("ids/test.png")
    blob.upload_from_filename.assert_called_once_with("/tmp/test.png")
    blob.make_public.assert_called_once_with()

    assert result == (
        "https://storage.googleapis.com/test-bucket/ids/test.png"
    )


def test_upload_to_gcs_propagates_client_errors(monkeypatch):
    monkeypatch.setenv(
        "GOOGLE_APPLICATION_CREDENTIALS",
        "/tmp/service-account.json",
    )

    with patch(
        "services.gcs.storage.Client.from_service_account_json",
        side_effect=RuntimeError("GCS unavailable"),
    ):
        try:
            upload_to_gcs(
                "/tmp/test.png",
                "test-bucket",
                "ids/test.png",
            )
        except RuntimeError as exc:
            assert str(exc) == "GCS unavailable"
        else:
            raise AssertionError("Expected GCS error to propagate")
