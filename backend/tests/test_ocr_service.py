import sys
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1]),
)

from services.ocr import extract_from_id


def test_extract_from_id_extracts_all_supported_fields():
    image = Mock()

    with (
        patch("services.ocr.Image.open", return_value=image) as image_open,
        patch(
            "services.ocr.pytesseract.image_to_string",
            return_value=(
                "Name: Mohamed Ahmed\n"
                "Email: mohamed@example.com\n"
                "Adults: 3\n"
            ),
        ) as image_to_string,
    ):
        result = extract_from_id("identity.png")

    image_open.assert_called_once_with("identity.png")
    image_to_string.assert_called_once_with(image, lang="eng")

    assert result == {
        "email": "mohamed@example.com",
        "no_of_adults": 3,
        "full_name": "Mohamed Ahmed",
        "raw_text": (
            "Name: Mohamed Ahmed\n"
            "Email: mohamed@example.com\n"
            "Adults: 3\n"
        ),
    }


def test_extract_from_id_returns_none_for_missing_optional_fields():
    image = Mock()

    with (
        patch("services.ocr.Image.open", return_value=image),
        patch(
            "services.ocr.pytesseract.image_to_string",
            return_value="Unstructured identity text",
        ),
    ):
        result = extract_from_id("identity.png")

    assert result == {
        "email": None,
        "no_of_adults": None,
        "full_name": None,
        "raw_text": "Unstructured identity text",
    }


def test_extract_from_id_propagates_ocr_errors():
    with (
        patch("services.ocr.Image.open", return_value=Mock()),
        patch(
            "services.ocr.pytesseract.image_to_string",
            side_effect=RuntimeError("OCR failed"),
        ),
    ):
        try:
            extract_from_id("identity.png")
        except RuntimeError as exc:
            assert str(exc) == "OCR failed"
        else:
            raise AssertionError("Expected OCR error to propagate")
