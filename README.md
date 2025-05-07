# 🩺 OCR Medical Specialty Detection

This app uses PaddleOCR and fuzzy matching to extract and detect medical specialties from scanned prescriptions (French/Arabic).

## How to use

1. Upload a prescription image (JPEG/PNG).
2. The app performs OCR and shows the extracted specialty.
3. All processing is done in-browser via Streamlit.

## Models
- OCR: PaddleOCR (PP-OCRv4)
- Matching: RapidFuzz with enriched lexicon

