import requests
from config import OPENROUTER_API_KEY

class LLMSummarizer:
    def __init__(self):
        self.api_key = OPENROUTER_API_KEY
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "meta-llama/llama-3.1-70b-instruct"  # Updated model name
    
    def summarize_document(self, text, doc_type, doc_number):
        """Summarize circular or notification text using OpenRouter"""
        
        prompt = f"""You are a tax expert. Summarize the following {doc_type} ({doc_number}) in 3-4 clear sentences.

Focus on:
1. What is the main change or update?
2. Who is affected?
3. What action is required?
4. Important dates/deadlines (if any)

Document text:
{text[:5000]}

Provide a professional summary:"""
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/yourusername/tax-newsletter",  # Replace with your repo
                "X-Title": "Tax Newsletter Automation"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            
            response = requests.post(self.base_url, json=payload, headers=headers, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            summary = result['choices'][0]['message']['content'].strip()
            return summary
            
        except Exception as e:
            print(f"Error summarizing with OpenRouter: {e}")
            return "Summary unavailable due to API error"
