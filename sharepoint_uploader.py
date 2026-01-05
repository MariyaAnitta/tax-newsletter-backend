import requests
from datetime import datetime
import config

class SharePointUploader:
    def __init__(self):
        self.webhook_url = config.POWER_AUTOMATE_WEBHOOK
    
    def format_newsletter_content(self, processed_data):
        """Format the newsletter data into readable text"""
        content = []
        content.append("=" * 70)
        content.append("INCOME TAX INDIA - DAILY NEWSLETTER")
        content.append(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p IST')}")
        content.append("=" * 70)
        content.append("\n")
        
        # Group by type
        circulars = [d for d in processed_data if d['type'] == 'Circular']
        notifications = [d for d in processed_data if d['type'] == 'Notification']
        releases = [d for d in processed_data if d['type'] == 'Press Release']
        
        # Circulars section
        if circulars:
            content.append(f"📋 NEW CIRCULARS ({len(circulars)})")
            content.append("-" * 70)
            for i, item in enumerate(circulars, 1):
                content.append(f"\n{i}. {item['number']}")
                content.append(f"   Date: {item['date']}")
                content.append(f"   Summary: {item['summary']}")
                content.append(f"   PDF: {item.get('pdf_url', 'N/A')}")
            content.append("\n")
        
        # Notifications section
        if notifications:
            content.append(f"📢 NEW NOTIFICATIONS ({len(notifications)})")
            content.append("-" * 70)
            for i, item in enumerate(notifications, 1):
                content.append(f"\n{i}. {item['number']}")
                content.append(f"   Date: {item['date']}")
                content.append(f"   Summary: {item['summary']}")
                content.append(f"   PDF: {item.get('pdf_url', 'N/A')}")
            content.append("\n")
        
        # Press Releases section
        if releases:
            content.append(f"🗞️ NEW PRESS RELEASES ({len(releases)})")
            content.append("-" * 70)
            for i, item in enumerate(releases, 1):
                content.append(f"\n{i}. {item.get('title', 'Untitled')}")
                content.append(f"   Date: {item['date']}")
            content.append("\n")
        
        content.append("=" * 70)
        content.append("End of Newsletter")
        content.append("=" * 70)
        
        return "\n".join(content)
    
    def upload_to_sharepoint(self, processed_data):
        """Upload newsletter to SharePoint via Power Automate"""
        try:
            # Format the content
            newsletter_content = self.format_newsletter_content(processed_data)
            
            # Prepare filename with today's date
            filename = f"Tax_Newsletter_{datetime.now().strftime('%Y-%m-%d')}.txt"
            
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
