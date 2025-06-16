# Chatpdf!

**Chatpdf** is a Streamlit-based web app that allows users to upload a PDF document, ask questions about its content, and receive instant, context-aware answers powered by a Google Generative AI model and retrieval-augmented generation (RAG).

**streamlit link**  
https://pdfreading.streamlit.app/

---

## Features

- Upload any PDF file for instant question answering.
- Ask natural language questions about the PDF content.
- Get precise answers generated using Google’s Gemini language models.
- View Rouge scores for the generated answers to evaluate quality.
- Simple and intuitive user interface using Streamlit.
- Temporary PDF uploads handled securely and cleaned up automatically.

---

## How It Works

1. User uploads a PDF file.
2. User inputs a question about the PDF.
3. The backend:
   - Extracts text and chunks from the PDF.
   - Embeds the content using Google Generative AI embedding models.
   - Uses a RAG pipeline to generate a relevant response.
4. The response and supporting context documents are shown.
5. Rouge scores are computed between the response and context as a quality metric.

---
