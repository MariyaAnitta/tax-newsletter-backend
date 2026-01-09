import requests
import PyPDF2
import io

class PDFProcessor:
    
    def download_pdf(self, url):
        """Download PDF from URL"""
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response.content
        except Exception as e:
            print(f"Error downloading PDF from {url}: {e}")
            return None
    
    def extract_text(self, pdf_content):
        """Extract text from PDF bytes"""
        try:
            pdf_file = io.BytesIO(pdf_content)
            reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
        except Exception as e:
            print(f"Error extracting text: {e}")
            return None
    
    def find_circular_pdf_url(self, circular_number):
        """Construct PDF URL for circular"""
        number = circular_number.replace('Circular No.', '').replace(' ', '').replace(':', '').replace('/', '-').strip()
        url = f"https://incometaxindia.gov.in/communications/circular/circular-{number.lower()}.pdf"
        return url
    
    def find_notification_pdf_url(self, notification_number):
        """Construct PDF URL for notification"""
        number = notification_number.replace('Notification No.', '').split('[')[0].replace(' ', '').replace(':', '').replace('/', '-').strip()
        
        # NEW: Handle leading zeros (05-2026 → 5-2026, 04-2026 → 4-2026)
        parts = number.split('-')
        if len(parts) >= 2:
            parts[0] = parts[0].lstrip('0') or '0'  # Remove leading zeros
            number = '-'.join(parts)
        
        url = f"https://incometaxindia.gov.in/communications/notification/notification-{number.lower()}.pdf"
        return url
