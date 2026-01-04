import google.generativeai as genai
from config import GEMINI_API_KEY

class GeminiSummarizer:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def summarize_document(self, text, doc_type, doc_number):
        """Summarize circular or notification text"""
        
        prompt = f"""
You are a tax expert. Summarize the following {doc_type} ({doc_number}) in 3-4 clear sentences.

Focus on:
1. What is the main change or update?
2. Who is affected?
3. What action is required?
4. Important dates/deadlines (if any)

Document text:
{text[:5000]}

Provide a professional summary:
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error summarizing: {e}")
            return "Summary unavailable"
