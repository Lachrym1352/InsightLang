from pdfminer.high_level import extract_text as pdf_extract_text
import fitz  # PyMuPDF
import re
import os

def extract_text(pdf_path):
    """PDF에서 텍스트 추출."""
    return pdf_extract_text(pdf_path)

def extract_images_from_pdf(pdf_path, output_folder="images/"):
    """PDF에서 이미지를 추출하여 저장."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    pdf_document = fitz.open(pdf_path)
    image_paths = []
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        images = page.get_images(full=True)
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_filename = f"{output_folder}page_{page_num+1}_img_{img_index+1}.png"
            with open(image_filename, "wb") as f:
                f.write(image_bytes)
            image_paths.append(image_filename)
    return image_paths

def protect_math_expressions(text):
    """수식을 보호하기 위해 플레이스홀더로 대체."""
    math_patterns = re.findall(r'\$.*?\$', text)
    placeholders = {f"[[FORMULA_{i}]]": formula for i, formula in enumerate(math_patterns)}
    for placeholder, formula in placeholders.items():
        text = text.replace(formula, placeholder)
    return text, placeholders

def restore_math_expressions(text, placeholders):
    """플레이스홀더를 원래 수식으로 복원."""
    for placeholder, formula in placeholders.items():
        text = text.replace(placeholder, formula)
    return text
