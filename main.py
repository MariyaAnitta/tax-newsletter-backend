import ssl
import certifi
from browse_ai_handler import BrowseAIHandler
from pdf_processor import PDFProcessor
#from gemini_summarizer import GeminiSummarizer
from llm_summarizer import LLMSummarizer
from email_sender import EmailSender
from sharepoint_uploader import SharePointUploader  # NEW LINE
from config import CIRCULARS_ROBOT_ID, NOTIFICATIONS_ROBOT_ID, PRESS_RELEASES_ROBOT_ID


class TaxNewsletterProcessor:
    def __init__(self):
        self.browse_ai = BrowseAIHandler()
        self.pdf_processor = PDFProcessor()
        #self.summarizer = GeminiSummarizer()
        self.summarizer = LLMSummarizer()  
        self.email_sender = EmailSender()
        self.sharepoint_uploader = SharePointUploader()  # NEW LINE
        self.processed_data = []
    
    def process_circulars(self):
        """Process circulars from Browse AI (ALL NEW items)"""
        print("\n📋 Processing Circulars...")
        print("-" * 60)
        
        circulars = self.browse_ai.get_captured_data(CIRCULARS_ROBOT_ID, new_only=True)
        #circulars = self.browse_ai.get_captured_data(CIRCULARS_ROBOT_ID, new_only=False)

        
        if not circulars:
            print("No new circulars found")
            return
        
        print(f"Found {len(circulars)} NEW circulars\n")
        
        for circular in circulars:
            circular_num = circular.get('Circular Number', '').strip()
            date = circular.get('Publish Date', '').strip()
            
            if not circular_num:
                continue
            
            print(f"Processing: {circular_num}")
            
            pdf_url = self.pdf_processor.find_circular_pdf_url(circular_num)
            pdf_content = self.pdf_processor.download_pdf(pdf_url)
            
            if pdf_content:
                text = self.pdf_processor.extract_text(pdf_content)
                
                if text and len(text) > 100:
                    print(f"  ✅ Extracted {len(text)} characters")
                    print(f"  🤖 Summarizing...")
                    summary = self.summarizer.summarize_document(text, "circular", circular_num)
                    
                    self.processed_data.append({
                        'type': 'Circular',
                        'number': circular_num,
                        'date': date,
                        'summary': summary,
                        'pdf_url': pdf_url
                    })
                    print(f"  ✅ Summarized!\n")
                else:
                    print(f"  ❌ Text extraction failed\n")
            else:
                print(f"  ❌ PDF download failed\n")
    
    def process_notifications(self):
        """Process notifications from Browse AI (ALL NEW items)"""
        print("\n📢 Processing Notifications...")
        print("-" * 60)
        
        notifications = self.browse_ai.get_captured_data(NOTIFICATIONS_ROBOT_ID, new_only=True)
        #notifications = self.browse_ai.get_captured_data(NOTIFICATIONS_ROBOT_ID, new_only=False)

        
        if not notifications:
            print("No new notifications found")
            return
        
        print(f"Found {len(notifications)} NEW notifications\n")
        
        for notification in notifications:
            notif_num = notification.get('Notification Number', '').strip()
            date = notification.get('Publish Date', '').strip()
            
            if not notif_num:
                continue
            
            print(f"Processing: {notif_num}")
            
            pdf_url = self.pdf_processor.find_notification_pdf_url(notif_num)
            pdf_content = self.pdf_processor.download_pdf(pdf_url)
            
            if pdf_content:
                text = self.pdf_processor.extract_text(pdf_content)
                
                if text and len(text) > 100:
                    print(f"  ✅ Extracted {len(text)} characters")
                    print(f"  🤖 Summarizing...")
                    summary = self.summarizer.summarize_document(text, "notification", notif_num)
                    
                    self.processed_data.append({
                        'type': 'Notification',
                        'number': notif_num,
                        'date': date,
                        'summary': summary,
                        'pdf_url': pdf_url
                    })
                    print(f"  ✅ Summarized!\n")
                else:
                    print(f"  ❌ Text extraction failed\n")
            else:
                print(f"  ❌ PDF download failed\n")
    
    def process_press_releases(self):
        """Process press releases from Browse AI (ALL NEW items)"""
        print("\n🗞️ Processing Press Releases...")
        print("-" * 60)
        
        releases = self.browse_ai.get_captured_data(PRESS_RELEASES_ROBOT_ID, new_only=True)
       # releases = self.browse_ai.get_captured_data(PRESS_RELEASES_ROBOT_ID, new_only=False)

        
        if not releases:
            print("No new press releases found")
            return
        
        print(f"Found {len(releases)} NEW press releases\n")
        
        for release in releases:
            title = release.get('Title', '').strip()
            date = release.get('Date', '').strip()
            
            if not title:
                continue
            
            print(f"Processing: {title[:60]}...")
            
            self.processed_data.append({
                'type': 'Press Release',
                'title': title,
                'date': date,
                'summary': title
            })
            print(f"  ✅ Added\n")
    
    def run(self):
        """Run the entire processing pipeline"""
        print("=" * 60)
        print("🚀 TAX NEWSLETTER PROCESSOR")
        print("=" * 60)
        
        self.process_circulars()
        self.process_notifications()
        self.process_press_releases()
        
        print("\n" + "=" * 60)
        
        if self.processed_data:
            print(f"✅ Found {len(self.processed_data)} new items total")
            print("\nBreakdown:")
            circulars_count = len([d for d in self.processed_data if d['type'] == 'Circular'])
            notifications_count = len([d for d in self.processed_data if d['type'] == 'Notification'])
            releases_count = len([d for d in self.processed_data if d['type'] == 'Press Release'])
            
            if circulars_count > 0:
                print(f"  📋 Circulars: {circulars_count}")
            if notifications_count > 0:
                print(f"  📢 Notifications: {notifications_count}")
            if releases_count > 0:
                print(f"  🗞️ Press Releases: {releases_count}")
            
            # Send email
            print("\n📧 Sending email via SendGrid...")
            email_success = self.email_sender.send_newsletter(self.processed_data)
            
            if email_success:
                print("✅ Email sent successfully!")
            else:
                print("❌ Email sending failed!")
            
            # NEW: Upload to SharePoint
            print("\n📤 Uploading to SharePoint...")
            sharepoint_success = self.sharepoint_uploader.upload_to_sharepoint(self.processed_data)
            
            if sharepoint_success:
                print("✅ SharePoint upload successful!")
            else:
                print("⚠️ SharePoint upload had issues (check logs)")
                
        else:
            print("✅ No new items detected (all content unchanged)")
            print("📧 No email sent (nothing to report)")
            print("📤 No SharePoint upload (nothing to report)")
        
        print("=" * 60)
        print("✅ Processing complete!\n")


if __name__ == "__main__":
    processor = TaxNewsletterProcessor()
    processor.run()
