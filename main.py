import fitz  # PyMuPDF
import os
import json
from langdetect import detect
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def is_heading(text):
    """Basic rules to ignore paragraphs and long text."""
    return text and len(text) < 100 and not text.endswith('.')

def extract_headings(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text_blocks = []

        for page_num, page in enumerate(doc, start=1):
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                if "lines" not in block:
                    continue
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        if not is_heading(text):
                            continue
                        font_size = span["size"]
                        font = span["font"]
                        is_bold = "Bold" in font
                        lang = ""
                        try:
                            lang = detect(text)
                        except:
                            pass
                        text_blocks.append({
                            "text": text,
                            "font_size": font_size,
                            "font": font,
                            "is_bold": is_bold,
                            "lang": lang,
                            "page": page_num
                        })

        # Sort unique font sizes (descending)
        font_sizes = sorted(list(set(b["font_size"] for b in text_blocks)), reverse=True)
        size_to_level = {size: f"H{i+1}" for i, size in enumerate(font_sizes[:3])}

        outline = []
        seen = set()
        for block in text_blocks:
            level = size_to_level.get(block["font_size"])
            if not level:
                continue
            identifier = (block["text"], block["page"])
            if identifier in seen:
                continue
            seen.add(identifier)
            outline.append({
                "level": level,
                "text": block["text"],
                "page": block["page"]
            })

        title = outline[0]["text"] if outline else os.path.basename(pdf_path).replace(".pdf", "")
        return {
            "title": title,
            "outline": outline
        }

    except Exception as e:
        logging.error(f"Failed to process {pdf_path}: {e}")
        return {
            "title": "Error",
            "outline": []
        }

def process_all_pdfs(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_dir, filename)
            result = extract_headings(pdf_path)
            output_path = os.path.join(output_dir, filename.replace(".pdf", ".json"))
            with open(output_path, "w") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            logging.info(f"Processed {filename} → {os.path.basename(output_path)}")

if __name__ == "__main__":
    logging.info(f"Process started at {datetime.now().isoformat()}")
    process_all_pdfs("/app/input", "/app/output")
