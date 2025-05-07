import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
from paddleocr import PaddleOCR
from rapidfuzz import fuzz

# Load OCRs
ocr_fr = PaddleOCR(lang='latin', use_angle_cls=True)
ocr_ar = PaddleOCR(lang='arabic', use_angle_cls=True)

# Multilingual OCR
def ocr_paddle_multilang(pil_image):
    img = np.array(pil_image)  # Convert to NumPy for PaddleOCR
    result_fr = ocr_fr.ocr(img)
    text_fr = " ".join([line[1][0] for line in result_fr[0]]) if result_fr and result_fr[0] else ""
    result_ar = ocr_ar.ocr(img)
    text_ar = " ".join([line[1][0] for line in result_ar[0]]) if result_ar and result_ar[0] else ""
    return (text_fr + " " + text_ar).strip()

# Load specialities
csv_path = "specialites.csv"
df_specialites = pd.read_csv(csv_path)
specialites_keywords = {
    row['SpecialitePrincipale']: [kw.strip() for kw in row['Synonymes'].split(',')]
    for _, row in df_specialites.iterrows()
}

def detect_specialite(text, seuil=80):
    text = text.lower()
    for specialite, keywords in specialites_keywords.items():
        for keyword in keywords:
            if fuzz.partial_ratio(text, keyword.lower()) >= seuil:
                return specialite
    return "Spécialité inconnue"

# Streamlit App
st.title("🩺 Medical Speciality Detector")

uploaded_file = st.file_uploader("Upload a prescription image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    text_ocr = ocr_paddle_multilang(image)
    specialite = detect_specialite(text_ocr)

    st.markdown(f"### ✅ Detected Specialty: **{specialite}**")
    st.markdown("### 📝 Extracted Text:")
    st.write(text_ocr)
