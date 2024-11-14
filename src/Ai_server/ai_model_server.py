import os
from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModel
from werkzeug.utils import secure_filename
import torch
from pdfminer.high_level import extract_text

app = Flask(__name__)   #Flask application 생성

@app.route('/fileupload',methods = ['POST'])      #() 안의 주소에 접속하면 바로 아랫줄에 있는 함수 호출
# 파일 업로드
def file_upload():
    file = request.files['file']
    filename = secure_filename(file.filename)
    
    


# # GPU가 사용 가능하면 "cuda", 아니면 "cpu"로 설정
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# print(f"Using device: {device}")

# # 모델과 토크나이저 로드
# translation_tokenizer = AutoTokenizer.from_pretrained("google/mt5-base")
# translation_model = AutoModelForSeq2SeqLM.from_pretrained("google/mt5-base").to(device)

# summary_tokenizer = AutoTokenizer.from_pretrained("google/pegasus-xsum")
# summary_model = AutoModelForSeq2SeqLM.from_pretrained("google/pegasus-xsum").to(device)

# similarity_tokenizer = AutoTokenizer.from_pretrained("intfloat/multilingual-e5-large")
# similarity_model = AutoModel.from_pretrained("intfloat/multilingual-e5-large").to(device)

# app = Flask(__name__)

# # 번역 함수
# def translate_text(text, target_language="ko"):
#     text_with_lang = f"translate to {target_language}: {text}"
#     inputs = translation_tokenizer(text_with_lang, return_tensors="pt").to(device)
#     outputs = translation_model.generate(inputs.input_ids)
#     translated_text = translation_tokenizer.decode(outputs[0], skip_special_tokens=True)
#     return translated_text

# # 요약 함수
# def summarize_text(text):
#     inputs = summary_tokenizer(text, return_tensors="pt", truncation=True).to(device)
#     outputs = summary_model.generate(inputs.input_ids)
#     summary_text = summary_tokenizer.decode(outputs[0], skip_special_tokens=True)
#     return summary_text

# # 논문 텍스트를 임베딩 벡터로 변환하는 함수
# def embed_text(text):
#     inputs = similarity_tokenizer(text, return_tensors="pt", truncation=True).to(device)
#     with torch.no_grad():
#         embeddings = similarity_model(**inputs).last_hidden_state.mean(dim=1)
#     return embeddings

# # 예시: 특정 논문과 유사한 논문 추천
# def recommend_similar_papers(query_text, paper_texts):
#     query_embedding = embed_text(query_text)
#     paper_embeddings = [embed_text(paper) for paper in paper_texts]
#     similarities = [torch.cosine_similarity(query_embedding, paper_embedding).item() for paper_embedding in paper_embeddings]
#     similar_papers = sorted(zip(paper_texts, similarities), key=lambda x: x[1], reverse=True)
#     return similar_papers[:5]

# # 번역 및 요약 엔드포인트
# @app.route("/translate_summarize", methods=["POST"])
# def translate_and_summarize():
#     data = request.get_json()
#     text = data.get("text", "")
#     target_language = data.get("target_language", "ko")
#     translated_text = translate_text(text, target_language)
#     summary_text = summarize_text(translated_text)
#     response = {
#         "translated_text": translated_text,
#         "summary": summary_text
#     }
#     return jsonify(response)

# # 기본 테스트 엔드포인트
# @app.route("/")
# def hello():
#     return "Hello, World!"

# if __name__ == "__main__":
#     print("Starting AI Model Server...")  # 디버깅용 출력
#     app.run(host="0.0.0.0", port=5001, debug=True)
