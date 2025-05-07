import streamlit as st
import cv2
import numpy as np
import pandas as pd
from PIL import Image
from paddleocr import PaddleOCR
from rapidfuzz import fuzz

# ⬇ Charger OCR français + arabe
ocr_fr = PaddleOCR(lang='latin', use_angle_cls=True)
ocr_ar = PaddleOCR(lang='arabic', use_angle_cls=True)

# 🔁 Détection OCR multilangue
def ocr_paddle_multilang(image):
    result_fr = ocr_fr.ocr(image)
    text_fr = " ".join([line[1][0] for line in result_fr[0]]) if result_fr and result_fr[0] else ""
    result_ar = ocr_ar.ocr(image)
    text_ar = " ".join([line[1][0] for line in result_ar[0]]) if result_ar and result_ar[0] else ""
    return (text_fr + " " + text_ar).strip()

# 📚 Charger CSV spécialités
csv_path = 'C:/Users/Malek/Desktop/4DS/PI/ocr_specialite_app/specialites.csv'  # adapter si besoin
df_specialites = pd.read_csv(csv_path)
specialites_keywords = {
    row['SpecialitePrincipale']: [kw.strip() for kw in row['Synonymes'].split(',')]
    for _, row in df_specialites.iterrows()
}

# 🔍 Détection avec fuzzy matching
def detect_specialite(text, seuil=80):
    text = text.lower()
    for specialite, keywords in specialites_keywords.items():
        for keyword in keywords:
            if fuzz.partial_ratio(text, keyword.lower()) >= seuil:
                return specialite
    return "Spécialité inconnue"

# ===============================
# 🎯 Interface Streamlit
# ===============================
st.title("🩺 Medical Speciality Detector ")

uploaded_file = st.file_uploader("Upload a prescription image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Afficher image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Convertir en format utilisable pour OpenCV
    img_array = np.array(image)
    image_cv2 = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

    # 🔍 OCR + spécialité
    text_ocr = ocr_paddle_multilang(image_cv2)
    specialite = detect_specialite(text_ocr)

    st.markdown(f"### ✅ Detected Specialty: **{specialite}**")
    st.markdown("### 📝 Extracted Text:")
    st.write(text_ocr)
