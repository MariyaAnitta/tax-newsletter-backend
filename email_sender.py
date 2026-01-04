import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from config import SENDGRID_API_KEY, EMAIL_FROM, EMAIL_TO

class EmailSender:
    def __init__(self):
        self.smtp_server = "smtp.sendgrid.net"
        self.smtp_port = 587
        self.username = "apikey"
        self.password = SENDGRID_API_KEY
        self.from_email = EMAIL_FROM
        self.to_email = EMAIL_TO
    
    def send_newsletter(self, newsletter_data):
        """Send tax newsletter via SendGrid SMTP"""
        
        if not newsletter_data:
            print("⚠️ No new data to send")
            return False
        
        # Group by type
        circulars = [d for d in newsletter_data if d['type'] == 'Circular']
        notifications = [d for d in newsletter_data if d['type'] == 'Notification']
        releases = [d for d in newsletter_data if d['type'] == 'Press Release']
        
        # Build email
        subject = f"🚨 India Tax Alert - {datetime.now().strftime('%B %d, %Y')}"
        html_body = self._build_html(circulars, notifications, releases)
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.from_email
            msg['To'] = self.to_email
            
            # Attach HTML
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)
            
            # Create SSL context with verification disabled (for corporate proxy)
            context = ssl._create_unverified_context()
            
            # Send email via SendGrid SMTP
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.ehlo()
                server.starttls(context=context)  # Use unverified context
                server.ehlo()
                server.login(self.username, self.password)
                server.send_message(msg)
            
            print(f"✅ Email sent successfully to {self.to_email}!")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send email: {e}")
            return False
    
    def _build_html(self, circulars, notifications, releases):
        """Build professional HTML email content"""
        
        total_items = len(circulars) + len(notifications) + len(releases)
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
               line-height: 1.6; color: #2c3e50; background: #f4f7fa; }}
        .container {{ max-width: 700px; margin: 0 auto; background: white; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                   color: white; padding: 40px 30px; text-align: center; }}
        .header h1 {{ font-size: 28px; margin-bottom: 10px; font-weight: 600; }}
        .header p {{ font-size: 16px; opacity: 0.95; }}
        .badge {{ background: rgba(255,255,255,0.2); 
                 padding: 8px 16px; border-radius: 20px; 
                 display: inline-block; margin-top: 15px; font-size: 14px; }}
        .content {{ padding: 30px; }}
        .section {{ margin-bottom: 40px; }}
        .section-header {{ display: flex; align-items: center; 
                          padding: 15px 20px; background: #f8f9fa;
                          border-left: 5px solid #667eea; margin-bottom: 20px; }}
        .section-header h2 {{ font-size: 20px; color: #2c3e50; 
                             margin-left: 10px; font-weight: 600; }}
        .item-card {{ background: #ffffff; border: 1px solid #e1e8ed;
                     border-radius: 8px; padding: 20px; margin-bottom: 15px;
                     box-shadow: 0 2px 4px rgba(0,0,0,0.08); }}
        .item-number {{ font-size: 16px; font-weight: 600; 
                       color: #667eea; margin-bottom: 8px; }}
        .item-date {{ color: #7f8c8d; font-size: 13px; 
                     margin-bottom: 12px; }}
        .item-summary {{ color: #34495e; font-size: 14px; 
                        line-height: 1.7; margin-bottom: 15px; }}
        .pdf-button {{ display: inline-block; background: #667eea;
                      color: white; padding: 10px 20px; 
                      text-decoration: none; border-radius: 5px;
                      font-size: 14px; font-weight: 500; }}
        .footer {{ background: #2c3e50; color: #ecf0f1; 
                  padding: 25px; text-align: center; }}
        .footer p {{ font-size: 13px; margin: 5px 0; opacity: 0.9; }}
        .emoji {{ font-size: 24px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🇮🇳 India Tax Newsletter</h1>
            <p>{datetime.now().strftime('%A, %B %d, %Y')}</p>
            <div class="badge">
                {total_items} New Update{'s' if total_items != 1 else ''} Available
            </div>
        </div>
        
        <div class="content">
"""
        
        # Circulars
        if circulars:
            html += f"""
            <div class="section">
                <div class="section-header">
                    <span class="emoji">📋</span>
                    <h2>New Circulars ({len(circulars)})</h2>
                </div>
"""
            for item in circulars:
                html += f"""
                <div class="item-card">
                    <div class="item-number">{item['number']}</div>
                    <div class="item-date">📅 {item['date']}</div>
                    <div class="item-summary">{item['summary']}</div>
                    <a href="{item['pdf_url']}" class="pdf-button">📄 View PDF</a>
                </div>
"""
            html += "</div>"
        
        # Notifications
        if notifications:
            html += f"""
            <div class="section">
                <div class="section-header">
                    <span class="emoji">📢</span>
                    <h2>New Notifications ({len(notifications)})</h2>
                </div>
"""
            for item in notifications:
                html += f"""
                <div class="item-card">
                    <div class="item-number">{item['number']}</div>
                    <div class="item-date">📅 {item['date']}</div>
                    <div class="item-summary">{item['summary']}</div>
                    <a href="{item['pdf_url']}" class="pdf-button">📄 View PDF</a>
                </div>
"""
            html += "</div>"
        
        # Press Releases
        if releases:
            html += f"""
            <div class="section">
                <div class="section-header">
                    <span class="emoji">🗞️</span>
                    <h2>Press Releases ({len(releases)})</h2>
                </div>
"""
            for item in releases:
                html += f"""
                <div class="item-card">
                    <div class="item-number">{item['title']}</div>
                    <div class="item-date">📅 {item['date']}</div>
                </div>
"""
            html += "</div>"
        
        html += """
        </div>
        <div class="footer">
            <p><strong>Automated Tax Monitoring System</strong></p>
            <p>Powered by Browse AI • Gemini AI</p>
        </div>
    </div>
</body>
</html>
"""
        return html
