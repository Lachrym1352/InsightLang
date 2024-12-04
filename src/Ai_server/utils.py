import fitz  # PyMuPDF
import os

if not os.path.exists("temp"):
    os.makedirs("temp")

def extract_text(pdf_path):
    """PDF 파일에서 텍스트 추출."""
    with fitz.open(pdf_path) as pdf:
        return "\n".join(page.get_text() for page in pdf)

def protect_math_expressions(text):
    """수식을 플레이스홀더로 대체."""
    placeholders = {}
    # 임시적으로 수식을 식별하고 플레이스홀더로 대체
    # 예제에서는 단순한 정규 표현식 사용
    placeholder_pattern = "[MATH-{index}]"
    # 실제 수식 식별 로직 구현 필요
    return text, placeholders

def restore_math_expressions(text, placeholders):
    """수식 플레이스홀더 복원."""
    for placeholder, original in placeholders.items():
        text = text.replace(placeholder, original)
    return text

def extract_images_with_positions_from_pdf(pdf_path):
    """PDF에서 이미지와 위치 정보를 추출."""
    images = []
    try:
        with fitz.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf, start=1):
                for img_index, img in enumerate(page.get_images(full=True), start=1):
                    xref = img[0]
                    base_image = pdf.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    image_path = f"temp/graph_page{page_num}_img{img_index}.{image_ext}"
                    with open(image_path, "wb") as f:
                        f.write(image_bytes)

                    # 그래프 위치 플레이스홀더 추가
                    position_placeholder = f"[GRAPH-page{page_num}_img{img_index}]"
                    images.append({"path": image_path, "position": position_placeholder})
    except Exception as e:
        print(f"Error extracting images: {e}")
    return images
    


