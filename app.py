import streamlit as st
import os
from file_processor import FileProcessor
from Helper import ChatManager

# Configure page
st.set_page_config(page_title="Multi-File Upload & AI Chat",
                   page_icon="🤖",
                   layout="wide")

# Initialize session state
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = {}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "file_processor" not in st.session_state:
    st.session_state.file_processor = FileProcessor()
if "chat_manager" not in st.session_state:
    st.session_state.chat_manager = ChatManager()


def main():
    st.title("🤖 Multi-File Upload & AI Chat Assistant")
    st.markdown("Upload multiple files and chat with AI about their contents!")

    # Create two columns for layout
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("📁 File Upload & Management")

        # File uploader
        uploaded_files = st.file_uploader(
            "Choose files",
            accept_multiple_files=True,
            type=['txt', 'pdf', 'docx', 'xlsx', 'csv'],
            help="Supported formats: TXT, PDF, DOCX, XLSX, CSV")

        # Process uploaded files
        if uploaded_files:
            for uploaded_file in uploaded_files:
                if uploaded_file.name not in st.session_state.uploaded_files:
                    # Validate file size before processing
                    max_size = 10 * 1024 * 1024  # 10MB
                    if uploaded_file.size > max_size:
                        st.error(f"❌ {uploaded_file.name} is too large. Maximum size is 10MB.")
                        continue
                    
                    with st.spinner(f"Processing {uploaded_file.name}..."):
                        try:
                            # Reset file pointer before processing
                            uploaded_file.seek(0)
                            content = st.session_state.file_processor.process_file(uploaded_file)
                            
                            st.session_state.uploaded_files[uploaded_file.name] = {
                                "content": content,
                                "size": uploaded_file.size,
                                "type": uploaded_file.type if hasattr(uploaded_file, 'type') else 'unknown'
                            }
                            st.success(f"✅ {uploaded_file.name} uploaded successfully!")
                            
                        except Exception as e:
                            st.error(f"❌ Error processing {uploaded_file.name}: {str(e)}")
                            # Continue processing other files even if one fails
                            continue

        # Display uploaded files
        if st.session_state.uploaded_files:
            st.subheader("📋 Uploaded Files")
            for filename, file_info in st.session_state.uploaded_files.items():
                with st.expander(f"📄 {filename}"):
                    col_info1, col_info2 = st.columns(2)
                    with col_info1:
                        st.write(f"**Size:** {file_info['size']} bytes")
                    with col_info2:
                        st.write(f"**Type:** {file_info['type']}")

                    # Show content preview
                    content_preview = file_info['content'][:500] + "..." if len(
                        file_info['content']) > 500 else file_info['content']
                    st.text_area("Content Preview",
                                 content_preview,
                                 height=100,
                                 disabled=True)

                    # Remove file button
                    if st.button(f"🗑️ Remove {filename}",
                                 key=f"remove_{filename}"):
                        del st.session_state.uploaded_files[filename]
                        st.rerun()

        # Clear all files button
        if st.session_state.uploaded_files:
            if st.button("🗑️ Clear All Files"):
                st.session_state.uploaded_files = {}
                st.rerun()

    with col2:
        st.header("💬 AI Chat Assistant")

        # Check if Gemini API key is available
        api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
        if not api_key:
            st.warning("⚠️ GEMINI_API_KEY not found in environment variables. Please set it to use the chat feature.")
            return

        # Initialize chat manager with API key

        if not st.session_state.chat_manager.is_initialized():
            st.session_state.chat_manager.initialize(api_key)

        # Display chat history
        chat_container = st.container()
        with chat_container:
            if st.session_state.chat_history:
                for i, message in enumerate(st.session_state.chat_history):
                    if message["role"] == "user":
                        st.markdown(f"**You:** {message['content']}")
                    else:
                        st.markdown(f"**AI:** {message['content']}")
                    st.markdown("---")
            else:
                st.info("💡 Start a conversation by typing a message below!")

        # Chat input
        user_input = st.text_area("Type your message here...",
                                  height=100,
                                  key="chat_input")

        col_send, col_clear = st.columns([3, 1])
        with col_send:
            if st.button("📤 Send Message", type="primary"):
                if user_input.strip():
                    # Add user message to history
                    st.session_state.chat_history.append({
                        "role": "user",
                        "content": user_input
                    })

                    # Prepare context from uploaded files
                    file_context = ""
                    if st.session_state.uploaded_files:
                        file_context = "\n\nUploaded files context:\n"
                        for filename, file_info in st.session_state.uploaded_files.items(
                        ):
                            file_context += f"\n--- {filename} ---\n{file_info['content']}\n"

                    # Get AI response
                    with st.spinner("🤔 AI is thinking..."):
                        try:
                            ai_response = st.session_state.chat_manager.get_response(
                                user_input + file_context,
                                st.session_state.
                                chat_history[:
                                             -1]  # Exclude the current user message
                            )

                            # Add AI response to history
                            st.session_state.chat_history.append({
                                "role":
                                "assistant",
                                "content":
                                ai_response
                            })

                        except Exception as e:
                            st.error(f"❌ Error getting AI response: {str(e)}")
                            # Remove the user message if AI response failed
                            st.session_state.chat_history.pop()

                    # Clear input and rerun
                    st.rerun()
                else:
                    st.warning("⚠️ Please enter a message!")

        with col_clear:
            if st.button("🗑️ Clear Chat"):
                st.session_state.chat_history = []
                st.rerun()

        # Chat statistics
        if st.session_state.chat_history:
            st.markdown("---")
            st.caption(
                f"💬 Total messages: {len(st.session_state.chat_history)}")


if __name__ == "__main__":
    main()



