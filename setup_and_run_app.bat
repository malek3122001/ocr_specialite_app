@echo off
echo =========================================
echo 🔧 Setting up OCR Specialty App (Python)
echo =========================================

REM 1. Create virtual environment
python -m venv ocr_env

REM 2. Activate it
call ocr_env\Scripts\activate

REM 3. Upgrade pip (optional but safe)
python -m pip install --upgrade pip

REM 4. Install required packages
pip install streamlit paddleocr paddlepaddle rapidfuzz opencv-python pandas

REM 5. Run the app
echo =========================================
echo 🚀 Launching Streamlit app...
echo =========================================
streamlit run app.py
