use actix_web::{web, App, HttpServer, HttpResponse, Responder}; 
use serde::{Deserialize, Serialize};    // JSON데이터를 구조체로 변환, 구조체를 JSON형식으로 변환
use reqwest;    //http 요청 보내는 라이브러리, ai_model_server와 통신

#[derive(Deserialize)] 
struct TranslateRequest {
    text: String,
    target_language: String,
}

#[derive(Serialize, Deserialize)]
struct TranslateResponse {
    translated_text: String,
    summary: String,
}   

// AI 모델 서버로 요청을 보내는 함수
async fn call_ai_model_server(text: &str, target_language: &str) -> Result<TranslateResponse, reqwest::Error> {
    let client = reqwest::Client::new();
    let request_body = serde_json::json!({
        "text": text,
        "target_language": target_language
    });

    let response = client
        .post("http://localhost:5001/translate_summarize")
        .json(&request_body)
        .send()
        .await?
        .json::<TranslateResponse>()
        .await?;

    Ok(response)
}   

// API 엔드포인트 핸들러
async fn translate_and_summarize(req: web::Json<TranslateRequest>) -> impl Responder {
    let text = &req.text;
    let target_language = &req.target_language;

    match call_ai_model_server(text, target_language).await {
        Ok(response) => HttpResponse::Ok().json(response),
        Err(_) => HttpResponse::InternalServerError().body("Error calling AI model server"),
    }
}

// 기본 경로에 대한 핸들러
async fn index() -> impl Responder {
    HttpResponse::Ok().body("Welcome to the Translation and Summarization API!")
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new()
            .route("/", web::get().to(index))   // 기본 경로
            .route("/translate", web::post().to(translate_and_summarize))   // 번역 및 요약 경로
    })
    .bind("127.0.0.1:8080")?
    .run()
    .await
}
