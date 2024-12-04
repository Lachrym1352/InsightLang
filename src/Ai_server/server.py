from fastapi import FastAPI, HTTPException, UploadFile, File
from src.Ai_server.models import batch_translate_texts, split_text
from src.Ai_server.utils import extract_text, protect_math_expressions, restore_math_expressions
import os

app = FastAPI()

@app.post("/process")
async def process_file(file: UploadFile = File(...)):
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, file.filename)

    try:
        # 파일 저장
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # 텍스트 추출 및 수식 보호
        extracted_text = extract_text(file_path)
        protected_text, placeholders = protect_math_expressions(extracted_text)

        # 텍스트 분할 및 배치 번역
        text_parts = split_text(protected_text)
        translated_parts = batch_translate_texts(text_parts)

        # 번역된 텍스트 병합
        restored_translated_text = " ".join(restore_math_expressions(part, placeholders) for part in translated_parts)

        # 결과 반환
        return {
            "original_text": extracted_text,
            "translated_text": restored_translated_text,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
    finally:
        # 파일 삭제
        if os.path.exists(file_path):
            os.remove(file_path)
