import os
from dotenv import load_dotenv

load_dotenv()

# Browse AI
BROWSE_AI_API_KEY = os.getenv('BROWSE_AI_API_KEY')
CIRCULARS_ROBOT_ID = os.getenv('CIRCULARS_ROBOT_ID')
NOTIFICATIONS_ROBOT_ID = os.getenv('NOTIFICATIONS_ROBOT_ID')
PRESS_RELEASES_ROBOT_ID = os.getenv('PRESS_RELEASES_ROBOT_ID')

# Gemini AI
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# SendGrid Email
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
EMAIL_FROM = os.getenv('EMAIL_FROM', 'noreply@taxalerts.com')
EMAIL_TO = os.getenv('EMAIL_TO')
POWER_AUTOMATE_WEBHOOK = os.getenv('POWER_AUTOMATE_WEBHOOK')