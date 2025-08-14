import os
from typing import List, Dict
import streamlit as st

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

class ChatManager:
    """Manages chat interactions with Google Gemini AI."""
    
    def __init__(self):
        self.model = None
        self.chat = None
        self._initialized = False
        
    def initialize(self, api_key: str):
        """
        Initialize the Gemini AI model with API key.
        
        Args:
            api_key: Google Gemini API key
        """
        if not GEMINI_AVAILABLE:
            raise Exception("Google Generative AI library not available. Please install google-generativeai.")
        
        try:
            # Configure the API key
            genai.configure(api_key=api_key)
            
            # Initialize the model
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Start a chat session
            self.chat = self.model.start_chat(history=[])
            
            self._initialized = True
            
        except Exception as e:
            raise Exception(f"Failed to initialize Gemini AI: {str(e)}")
    
    def is_initialized(self) -> bool:
        """Check if the chat manager is initialized."""
        return self._initialized
    
    def get_response(self, message: str, conversation_history: List[Dict[str, str]] = None) -> str:
        """
        Get AI response for a given message.
        
        Args:
            message: User message
            conversation_history: Previous conversation history
            
        Returns:
            str: AI response
        """
        if not self._initialized:
            raise Exception("ChatManager not initialized. Call initialize() first.")
        
        try:
            # Create a system prompt to guide the AI behavior
            system_prompt = """You are a helpful AI assistant that can analyze and discuss uploaded files. 
            You have access to the content of files that users have uploaded. When responding:
            1. Be helpful and informative
            2. Reference specific content from uploaded files when relevant
            3. Ask clarifying questions if needed
            4. Provide detailed explanations when analyzing file content
            5. Be concise but thorough in your responses
            
            If the user asks about files but no file content is provided, let them know you don't see any uploaded files.
            """
            # Prepare the conversation context
            if conversation_history:
                # Create a new chat with history for context
                history = []
                for msg in conversation_history:
                    if msg["role"] == "user":
                        history.append({
                            "role": "user",
                            "parts": [msg["content"]]
                        })
                    else:
                        history.append({
                            "role": "model",
                            "parts": [msg["content"]]
                        })
                
                # Create a new chat with history
                chat_with_history = self.model.start_chat(history=history)
                response = chat_with_history.send_message(system_prompt + "\n\nUser: " + message)
            else:
                # First message or no history
                response = self.chat.send_message(system_prompt + "\n\nUser: " + message)
            
            return response.text
            
        except Exception as e:
            # Handle different types of errors
            error_message = str(e).lower()
            
            if "api key" in error_message:
                raise Exception("Invalid or expired API key. Please check your GEMINI_API_KEY.")
            elif "quota" in error_message or "limit" in error_message:
                raise Exception("API quota exceeded. Please try again later.")
            elif "blocked" in error_message:
                raise Exception("Message was blocked by safety filters. Please rephrase your message.")
            else:
                raise Exception(f"Error getting AI response: {str(e)}")
    
    def clear_conversation(self):
        """Clear the conversation history."""
        if self._initialized:
            self.chat = self.model.start_chat(history=[])
    
    def get_model_info(self) -> Dict[str, str]:
        """Get information about the current model."""
        if not self._initialized:
            return {"status": "Not initialized"}
        
        return {
            "model": "gemini-1.5-flash",
            "status": "Initialized",
            "provider": "Google Generative AI"
        }
    
    @staticmethod
    def is_gemini_available() -> bool:
        """Check if Gemini library is available."""
        return GEMINI_AVAILABLE
    
    @staticmethod
    def get_setup_instructions() -> str:
        """Get setup instructions for Gemini API."""
        return """
        To use the Gemini AI chat feature:
        
        1. Get a Gemini API key from Google AI Studio (https://makersuite.google.com/app/apikey)
        2. Set the environment variable: GEMINI_API_KEY=your_api_key_here
        3. Make sure google-generativeai is installed: pip install google-generativeai
        
        The application will automatically use the API key from the environment variable.
        """
