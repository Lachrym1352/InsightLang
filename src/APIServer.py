from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from utils import extract_text, protect_math_expressions, restore_math_expressions
from models import batch_translate_texts, split_text
from fastapi.middleware.cors import CORSMiddleware
import os
import logging

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Live Server 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

@app.post("/process")
async def process_file(request: Request, file: UploadFile = File(...)):
    logger.info(f"Received request from: {request.client.host}")
    file_path = os.path.join(TEMP_DIR, file.filename)

    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())

        extracted_text = extract_text(file_path)
        protected_text, placeholders = protect_math_expressions(extracted_text)

        text_parts = split_text(protected_text)
        translated_parts = batch_translate_texts(text_parts)

        restored_translated_text = " ".join(restore_math_expressions(part, placeholders) for part in translated_parts)

        return {
            "original_text": extracted_text,
            "translated_text": restored_translated_text,
        }

    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Translation failed")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
