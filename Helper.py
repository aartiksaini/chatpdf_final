from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
import os
from PyPDF2 import PdfReader
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import google.generativeai as genai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from pathlib import Path

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
print(f"Using API key: {google_api_key}")

genai.configure(api_key=google_api_key)

try:
    model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
    response = model.generate_content("Hello")
    print(response.text)
except Exception as e:
    print("Error:", e)


def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as pdfFile:
        pdfReader = PdfReader(pdfFile)
        all_text = ""
        for page in pdfReader.pages:
            text = page.extract_text()
            if text:
                all_text += text.encode('ascii', 'ignore').decode('ascii') + "\n"
    return all_text


def get_text_chunks(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    return splitter.split_text(text)


def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(
        google_api_key=google_api_key, model="models/embedding-001"
    )
    return FAISS.from_texts(text_chunks, embedding=embeddings)


def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context.
    If the answer is not in the context, just say "answer is not available in the context".

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
    model = ChatGoogleGenerativeAI(
        google_api_key=google_api_key,
        model="gemini-pro",
        temperature=0.3
    )

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )
    return load_qa_chain(model, chain_type="stuff", prompt=prompt)


def user_input(user_question, pdf_path):
    # 1. Extract text from uploaded PDF
    pdf_text = extract_text_from_pdf(pdf_path)

    # 2. Split text into chunks
    chunks = get_text_chunks(pdf_text)

    # 3. Embed chunks and create temporary FAISS vector store
    vector_store = get_vector_store(chunks)

    # 4. Perform similarity search
    docs = vector_store.similarity_search(user_question)

    # 5. Get the conversational chain
    chain = get_conversational_chain()

    # 6. Get the response
    response = chain(
        {"input_documents": docs, "question": user_question},
        return_only_outputs=True
    )

    return response, docs
