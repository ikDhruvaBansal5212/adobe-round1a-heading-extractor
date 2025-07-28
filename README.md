# Adobe Hackathon – Round 1A Enhanced Heading Extractor

## 🚀 Description

This tool extracts structured outlines (title, H1, H2, H3 headings) from PDFs using:
- Font size clustering
- Bold font detection
- Position and language heuristics
- Multilingual support (e.g., Japanese, Hindi)

## 🧠 Features
- Detects headings in multiple languages
- Handles noisy PDFs (repetitive headers, paragraphs)
- Handles edge cases gracefully
- Works offline in Docker
- Logs processing progress

---

## 🐳 Docker Usage

### 1. Build the Docker Image

```bash
docker build --platform linux/amd64 -t heading-extractor:latest .
