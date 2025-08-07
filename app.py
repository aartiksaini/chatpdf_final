import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import HuggingFaceHub
from langchain.chains.question_answering import load_qa_chain
import evaluate
import os

# Load once to avoid multiple downloads
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

from langchain_community.llms import HuggingFaceHub

llm = HuggingFaceHub(
    repo_id="google/flan-t5-base",
    model_kwargs={"max_length": 512}
)


def process_pdf(pdf_path):
    pdf_reader = PdfReader(pdf_path)
    raw_text = ""

    for page in pdf_reader.pages:
        text = page.extract_text()
        if text:
            raw_text += text

    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=800, chunk_overlap=200, length_function=len
    )
    chunks = text_splitter.split_text(raw_text)

    return chunks

def create_vector_store(text_chunks):
    return FAISS.from_texts(text_chunks, embedding=embeddings)

def ask_question(question, pdf_path):
    chunks = process_pdf(pdf_path)
    vector_store = create_vector_store(chunks)
    docs = vector_store.similarity_search(question)
    chain = load_qa_chain(llm, chain_type="stuff")
    response = chain.run(input_documents=docs, question=question)
    return response, docs

def create_ui():
    st.title("📄 PDF made easy!")
    st.sidebar.write("### Upload a PDF and ask any question.")
    st.markdown("1. Upload a PDF file.\n2. Enter your question.\n3. Click 'Submit'.")

    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    question = st.text_input("Ask a question:")

    if st.button("Submit"):
        if not uploaded_file:
            st.error("Please upload a PDF first.")
        elif not question.strip():
            st.error("Please enter a question.")
        else:
            with st.spinner("Processing..."):
                temp_path = "temp_uploaded.pdf"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.read())

                response, context_docs = ask_question(question, temp_path)

                # ROUGE scoring
                rouge = evaluate.load("rouge")
                output_text = response
                context = ' '.join([doc.page_content for doc in context_docs])
                results = rouge.compute(predictions=[output_text], references=[context])

                st.success("Answer:")
                st.write(output_text)

                st.success("ROUGE score:")
                st.json(results)

                os.remove(temp_path)

    st.markdown("---")
    st.caption("Built by Aartik Saini")

def main():
    create_ui()

if __name__ == "__main__":
    main()

