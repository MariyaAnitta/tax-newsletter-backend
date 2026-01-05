from datetime import datetime

class HTMLFormatter:
    @staticmethod
    def format_newsletter_html(processed_data):
        """Format newsletter as HTML with professional styling"""
        
        # Group by type
        circulars = [d for d in processed_data if d['type'] == 'Circular']
        notifications = [d for d in processed_data if d['type'] == 'Notification']
        releases = [d for d in processed_data if d['type'] == 'Press Release']
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .header h1 {{
            margin: 0;
            font-size: 28px;
        }}
        .header p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
        }}
        .summary-box {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
            border-left: 5px solid #2a5298;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .summary-box h2 {{
            margin-top: 0;
            color: #1e3c72;
        }}
        .section {{
            background: white;
            padding: 25px;
            border-radius: 8px;
            margin-bottom: 25px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .section-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 20px;
            border-radius: 8px 8px 0 0;
            margin: -25px -25px 20px -25px;
            font-size: 20px;
            font-weight: bold;
        }}
        .item {{
            background: #f9f9f9;
            padding: 20px;
            border-radius: 6px;
            margin-bottom: 20px;
            border-left: 4px solid #667eea;
        }}
        .item h3 {{
            margin-top: 0;
            color: #1e3c72;
            font-size: 18px;
        }}
        .item-meta {{
            color: #666;
            font-size: 14px;
            margin-bottom: 15px;
        }}
        .item-summary {{
            line-height: 1.6;
            color: #333;
            margin-bottom: 15px;
        }}
        .pdf-link {{
            display: inline-block;
            background: #2a5298;
            color: white;
            padding: 8px 16px;
            border-radius: 4px;
            text-decoration: none;
            font-size: 14px;
        }}
        .pdf-link:hover {{
            background: #1e3c72;
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            color: #666;
            margin-top: 40px;
            border-top: 2px solid #e0e0e0;
        }}
        .badge {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            margin-right: 10px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📰 Income Tax India - Daily Tax Newsletter</h1>
        <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p IST')}</p>
    </div>
    
    <div class="summary-box">
        <h2>Summary</h2>
        <p><strong>Total New Items:</strong> {len(processed_data)}</p>
        <p>
            {"<span class='badge'>" + str(len(circulars)) + " Circulars</span>" if circulars else ""}
            {"<span class='badge'>" + str(len(notifications)) + " Notifications</span>" if notifications else ""}
            {"<span class='badge'>" + str(len(releases)) + " Press Releases</span>" if releases else ""}
        </p>
    </div>
"""
        
        # Circulars
        if circulars:
            html += """
    <div class="section">
        <div class="section-header">📋 New Circulars</div>
"""
            for i, item in enumerate(circulars, 1):
                html += f"""
        <div class="item">
            <h3>{item['number']}</h3>
            <div class="item-meta"> Date: {item['date']}</div>
            <div class="item-summary">{item['summary']}</div>
            <a href="{item.get('pdf_url', '#')}" class="pdf-link" target="_blank">📄 View PDF</a>
        </div>
"""
            html += "    </div>\n"
        
        # Notifications
        if notifications:
            html += """
    <div class="section">
        <div class="section-header">📢 New Notifications</div>
"""
            for i, item in enumerate(notifications, 1):
                html += f"""
        <div class="item">
            <h3>{item['number']}</h3>
            <div class="item-meta">Date: {item['date']}</div>
            <div class="item-summary">{item['summary']}</div>
            <a href="{item.get('pdf_url', '#')}" class="pdf-link" target="_blank">📄 View PDF</a>
        </div>
"""
            html += "    </div>\n"
        
        # Press Releases
        if releases:
            html += """
    <div class="section">
        <div class="section-header">🗞️ New Press Releases</div>
"""
            for i, item in enumerate(releases, 1):
                html += f"""
        <div class="item">
            <h3>{item.get('title', 'Untitled')}</h3>
            <div class="item-meta"> Date: {item['date']}</div>
        </div>
"""
            html += "    </div>\n"
        
        html += """
    <div class="footer">
        <p>End of Newsletter</p>
        <p>Generated automatically by Tax Monitoring System</p>
    </div>
</body>
</html>
"""
        return html
