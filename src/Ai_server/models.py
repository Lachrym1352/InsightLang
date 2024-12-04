import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# NLLB 모델 로드
MODEL_NAME = "facebook/nllb-200-distilled-600M"  # NLLB 모델 이름
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

translation_cache = {}  # 번역 캐시

def split_text(text, max_length=1000):
    """텍스트를 지정된 길이로 분할"""
    return [text[i:i + max_length] for i in range(0, len(text), max_length)]

def translate_text(text, source_lang="eng_Latn", target_lang="kor_Hang"):
    """NLLB를 사용하여 텍스트 번역"""
    try:
        if text in translation_cache:
            return translation_cache[text]  # 캐시된 번역 반환

        # 입력 텍스트를 토크나이저로 변환
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=1000)
        target_lang_id = tokenizer.convert_tokens_to_ids(f"{target_lang}")

        # 번역 수행
        translated_tokens = model.generate(**inputs, forced_bos_token_id=target_lang_id)
        translated_text = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)

        # 캐시에 저장
        translation_cache[text] = translated_text
        return translated_text

    except Exception as e:
        print(f"Translation Error: {e}")
        return "[Translation Failed]"

def batch_translate_texts(texts, source_lang="eng_Latn", target_lang="kor_Hang", batch_size=16):
    """배치 번역"""
    results = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        inputs = tokenizer(batch, return_tensors="pt", padding=True, truncation=True, max_length=1000)
        target_lang_id = tokenizer.convert_tokens_to_ids(f"{target_lang}")
        translated_tokens = model.generate(**inputs, forced_bos_token_id=target_lang_id)
        translated_texts = [tokenizer.decode(t, skip_special_tokens=True) for t in translated_tokens]
        results.extend(translated_texts)
    return results
