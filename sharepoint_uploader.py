import requests
from datetime import datetime
import config
from html_formatter import HTMLFormatter  # Add this import

class SharePointUploader:
    def __init__(self):
        self.webhook_url = config.POWER_AUTOMATE_WEBHOOK
        self.html_formatter = HTMLFormatter()  # Add this
    
    # Keep the existing format_newsletter_content for text version
    
    def upload_to_sharepoint(self, processed_data):
        """Upload newsletter to SharePoint via Power Automate"""
        try:
            # Generate HTML content
            newsletter_content = self.html_formatter.format_newsletter_html(processed_data)
            
            # Prepare filename with today's date - CHANGE TO .html
            filename = f"Tax_Newsletter_{datetime.now().strftime('%Y-%m-%d')}.html"
            
            # Prepare payload for Power Automate
            payload = {
                "filename": filename,
                "content": newsletter_content
            }
            
            # Send to Power Automate webhook
            print(f"📤 Uploading to SharePoint: {filename}")
            response = requests.post(self.webhook_url, json=payload, timeout=30)
            
            if response.status_code in [200, 202]:
                print("✅ Uploaded to SharePoint successfully!")
                return True
            else:
                print(f"⚠️ SharePoint upload failed: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error uploading to SharePoint: {str(e)}")
            return False
