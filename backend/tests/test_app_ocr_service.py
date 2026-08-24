import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1]),
)

from app.ocr_service import extract_text_from_image


def test_extract_text_from_image_extracts_adults(monkeypatch):
    monkeypatch.setattr(
        "app.ocr_service.Image.open",
        lambda path: "fake-image",
    )

    monkeypatch.setattr(
        "app.ocr_service.pytesseract.image_to_string",
        lambda image: "Adults: 4\nChildren: 2",
    )

    result = extract_text_from_image("fake-id.png")

    assert result == {"no_of_adults": 4}


def test_extract_text_from_image_defaults_to_zero(monkeypatch):
    monkeypatch.setattr(
        "app.ocr_service.Image.open",
        lambda path: "fake-image",
    )

    monkeypatch.setattr(
        "app.ocr_service.pytesseract.image_to_string",
        lambda image: "No adult count available",
    )

    result = extract_text_from_image("fake-id.png")

    assert result == {"no_of_adults": 0}
