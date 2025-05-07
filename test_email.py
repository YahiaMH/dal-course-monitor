import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import *

def send_test_email():
    """Send a test email to verify the email functionality"""
    try:
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECIPIENT
        msg['Subject'] = "Dal Course Monitor - Test Email"
        
        # Add message body
        message_body = f"""This is a test email from the Dal Course Monitor.

Course: {COURSE_NAME}
CRN: {CRN_TO_MONITOR}
Currently Monitoring: {VALUE_TO_MONITOR} value

If you're receiving this email, the notification system is working correctly!
You will receive an email notification when a seat becomes available.
        """
        msg.attach(MIMEText(message_body, 'plain'))
        
        # Connect to the SMTP server and send the email
        print(f"Sending test email to {EMAIL_RECIPIENT}...")
        
        # Gmail
        server = smtplib.SMTP(EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT)
        server.starttls()  # Enable TLS encryption
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_SENDER, EMAIL_RECIPIENT, text)
        server.quit()
            
        print(f"Test email sent successfully to {EMAIL_RECIPIENT}")
        return True
    except Exception as e:
        print(f"Failed to send test email: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing email notification functionality...")
    if send_test_email():
        print("Email test successful! You should receive an email shortly.")
    else:
        print("Email test failed. Please check your configuration settings.") 