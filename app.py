import streamlit as st
from Helper import user_input
import evaluate
import os

def create_ui():
    st.title("PDF made easy!")
    st.sidebar.write("### Welcome to PDF made easy!")
    st.sidebar.write("Ask a question below and get instant insights.")

    st.markdown("### Instructions")
    st.markdown("""
    1. Upload a PDF file.
    2. Enter your question in the text box below.
    3. Click on 'Submit' to get the response.
    """)

    # Step 1: Upload PDF
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    
    # Step 2: Ask a question
    question = st.text_input("Ask a question:")

    # Step 3: Submit button
    if st.button("Submit"):
        if uploaded_file is None:
            st.error("Please upload a PDF first.")
        elif question.strip() == "":
            st.error("Please enter a question.")
        else:
            with st.spinner("Generating response..."):
                # Save uploaded file temporarily
                temp_path = os.path.join("temp_uploaded.pdf")
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.read())
                
                # Call your helper function (make sure it returns response and context_docs)
                response, context_docs = user_input(question, temp_path)

                # Load ROUGE metric
                rouge = evaluate.load('rouge')

                output_text = response.get('output_text', 'No response')
                context = ' '.join([doc.page_content for doc in context_docs])

                # Compute ROUGE score
                results = rouge.compute(predictions=[output_text], references=[context])

                st.success("Response:")
                st.write(output_text)

                st.success("ROUGE score:")
                st.write(results)

                # Cleanup temporary file
                os.remove(temp_path)

    st.markdown("---")
    st.markdown("**Powered by**: Rohitash Bishnoi")

def main():
    create_ui()

if __name__ == "__main__":
    main()
