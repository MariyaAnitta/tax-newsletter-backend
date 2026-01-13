import requests
from config import OPENROUTER_API_KEY


class LLMSummarizer:
    def __init__(self):
        self.api_key = OPENROUTER_API_KEY
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "meta-llama/llama-3.1-70b-instruct"
    
    def summarize_document(self, text, doc_type, doc_number):
        """Summarize circular or notification text using OpenRouter"""
        
        prompt = f"""Summarize this tax {doc_type} in 2-3 clear, professional sentences. Write directly - no introductory phrases like "Here is a summary" or "The main update is". Focus on:

1. The specific change or update
2. Who is affected (taxpayers, entities, deadlines)
3. Required actions or important dates

Document text:
{text[:5000]}

Summary:"""
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/yourusername/tax-newsletter",
                "X-Title": "Tax Newsletter Automation"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a tax expert. Provide concise summaries without meta-commentary. Write directly and professionally."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.3
            }
            
            response = requests.post(self.base_url, json=payload, headers=headers, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            summary = result['choices'][0]['message']['content'].strip()
            
            # Clean up any remaining meta-phrases
            cleanup_phrases = [
                "Here is a summary:",
                "Here's a summary:",
                "Here is the summary:",
                "Here's the summary:",
                "Summary:",
                "The main update is that",
                "The main change is that",
                "In summary,",
                "To summarize,",
                "Here is a 2-3 sentence",
                "Here is a 3-4 sentence",
                "Here's a 2-3 sentence",
                "Here's a 3-4 sentence"
            ]
            
            for phrase in cleanup_phrases:
                if summary.lower().startswith(phrase.lower()):
                    summary = summary[len(phrase):].strip()
                    # Remove any trailing colon if present
                    if summary.startswith(':'):
                        summary = summary[1:].strip()
            
            return summary
            
        except Exception as e:
            print(f"Error summarizing with OpenRouter: {e}")
            return "Summary unavailable due to API error"
