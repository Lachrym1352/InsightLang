from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# 번역 모델 로드
translation_tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-tc-big-en-ko")
translation_model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-tc-big-en-ko")

# 요약 모델 로드
summary_tokenizer = AutoTokenizer.from_pretrained("google/pegasus-large")
summary_model = AutoModelForSeq2SeqLM.from_pretrained("google/pegasus-large")

def translate_text(text):
    """번역 텍스트 생성."""
    inputs = translation_tokenizer(text, return_tensors="pt", max_length=512, truncation=True)
    outputs = translation_model.generate(**inputs, max_length=512, num_beams=5)
    return translation_tokenizer.decode(outputs[0], skip_special_tokens=True)

def summarize_text(text, tokenizer, model, max_length=150, min_length=50, num_beams=5):
    """텍스트 요약."""
    inputs = tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(
        inputs["input_ids"], 
        max_length=max_length, 
        min_length=min_length, 
        num_beams=num_beams, 
        length_penalty=2.0, 
        early_stopping=True
    )
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

def split_and_summarize(text, max_chunk_length=512, max_length=150, min_length=50, num_beams=5):
    """긴 텍스트를 나누어 요약."""
    chunks = [text[i:i+max_chunk_length] for i in range(0, len(text), max_chunk_length)]
    summaries = [
        summarize_text(chunk, summary_tokenizer, summary_model, max_length, min_length, num_beams)
        for chunk in chunks
    ]
    return " ".join(summaries)
