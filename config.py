import os

# Dal Academic Timetable Monitor Configuration

# The URL of the academic timetable
URL = "https://self-service.dal.ca/BannerExtensibility/customPage/page/dal.stuweb_academicTimetable"

# How often to check for changes (in seconds)
CHECK_INTERVAL = 300  # 5 minutes

# Course information
CRN_TO_MONITOR = "30357"  # Replace with your course CRN
COURSE_NAME = "CSCI 4141 Information Retrieval"  # Replace with your course name

# What value to monitor (e.g., "Avail" seats, "WtLst" waitlist spots, etc.)
VALUE_TO_MONITOR = "Avail"  # Choose from: "Max", "Cur", "Avail", "WtLst", "%Full"

# Notification settings
NOTIFICATION_TITLE = "Course Availability Update"
NOTIFICATION_APP_NAME = "Dal Course Monitor"
NOTIFICATION_TIMEOUT = 10  # seconds

# Email notification settings
# Set to False to disable email notifications, True to enable
EMAIL_ENABLED = True

# Email credentials
EMAIL_SENDER = os.environ.get("EMAIL_SENDER")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
EMAIL_RECIPIENT = os.environ.get("EMAIL_RECIPIENT")

# Email server settings - Common providers:
# Gmail: smtp.gmail.com:587
# Outlook/Hotmail: smtp.office365.com:587
# Yahoo: smtp.mail.yahoo.com:587
EMAIL_SMTP_SERVER = "smtp.gmail.com"
EMAIL_SMTP_PORT = 587

# IMPORTANT: For Gmail, you'll need to:
# 1. Enable 2-Step Verification: https://myaccount.google.com/security
# 2. Create an App Password: https://myaccount.google.com/apppasswords
# 3. Use that App Password instead of your regular password

# Email-to-SMS Gateway (for text messages)
# To send to a phone number, use one of these email formats as EMAIL_RECIPIENT:
# AT&T: number@txt.att.net
# T-Mobile: number@tmomail.net
# Verizon: number@vtext.com
# Sprint: number@messaging.sprintpcs.com
# Example: "1234567890@txt.att.net" 