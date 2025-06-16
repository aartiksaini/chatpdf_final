# Chatpdf!

**Chatpdf** is a Streamlit-based web app that allows users to upload a PDF document, ask questions about its content, and receive instant, context-aware answers powered by a Google Generative AI model and retrieval-augmented generation (RAG).

**streamlit link**
https://rohitashbishnoi91-chatpdf-using-rag-app-j0q8fy.streamlit.app/
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

## Installation

Make sure you have Python 3.8+ installed. Then:

```bash
git clone https://github.com/your-repo/pdf-made-easy.git
cd pdf-made-easy
python -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
pip install -r requirements.txt
Setup Google Generative AI API
Go to Google Cloud Console.

Create or locate your API Key.

Enable the Generative Language API.

Make sure your API key has no restrictions that block your app.

Set your API key as an environment variable or directly in the code (helper.py):

python
Copy
Edit
GOOGLE_API_KEY = "YOUR_API_KEY"
Usage
Run the Streamlit app:

bash
Copy
Edit
streamlit run app.py
Upload your PDF.

Enter your question.

Click Submit to get an answer along with Rouge score.

Troubleshooting
API key expired or invalid:

Check your key in Google Cloud Console.

Verify API is enabled.

Test key validity via curl or Python script.

Ensure you’re using a currently supported model name from the latest list (e.g. models/gemini-1.5-pro-latest).

Model not found error:

Use ListModels API or check the console for available model names.

Update your model name in the code accordingly.

Project Structure
graphql
Copy
Edit
.
├── app.py                # Streamlit UI
├── helper.py             # Backend logic for PDF processing & querying Google API
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
└── temp_uploaded.pdf     # Temporary uploaded PDF (runtime only)
Dependencies
Streamlit

evaluate (for Rouge scoring)

requests (for API calls)

langchain (for RAG integration)

PyPDF2 or pdfplumber (for PDF parsing)

Other dependencies as per requirements.txt

Future Improvements
Add caching to speed up repeated queries.

Support more file types (e.g. DOCX).

Enhance error handling and UI feedback.

Add user authentication for API usage tracking.

Author
Rohitash Bishnoi
