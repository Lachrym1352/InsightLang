import os
from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModel
from werkzeug.utils import secure_filename
import torch
from pdfminer.high_level import extract_text

# Use a pipeline as a high-level helper
from transformers import pipeline

translation_pipeline = pipeline("text2text-generation", model="google/mt5-base")

summarization_pipeline = pipeline("summarization", model="google/pegasus-xsum")


app = Flask(__name__)

# 업로드된 파일을 저장할 디렉토리 설정
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 디렉토리가 없으면 생성
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/fileupload', methods=['POST'])
def file_upload():
    # 파일이 요청에 포함되어 있는지 확인
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    # 파일 이름이 비어 있는지 확인
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # 안전한 파일 이름 사용
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # 파일 저장
    file.save(file_path)

    # PDF에서 텍스트 추출
    try:
        extracted_text = extract_text(file_path)

         # 번역
        translated_text = translation_pipeline(extracted_text, max_length=512, truncation=True)[0]['translation_text']

        # 요약
        summary = summarization_pipeline(translated_text, max_length=150, min_length=50, truncation=True)[0]['summary_text']
    


        return jsonify({
            "original_text": extracted_text,
            "translated_text": translated_text,
            "summary": summary
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

    
    


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
