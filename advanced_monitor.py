import time
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from plyer import notification
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from config import *

# Current value will be updated during the first run
CURRENT_VALUE = None

def send_notification(title, message):
    """Send a desktop notification"""
    notification.notify(
        title=title,
        message=message,
        app_name=NOTIFICATION_APP_NAME,
        timeout=NOTIFICATION_TIMEOUT
    )
    print(f"{datetime.now()} - Notification sent: {title} - {message}")
    
    # Also send an email notification if configured
    if EMAIL_ENABLED:
        send_email_notification(title, message)

def send_email_notification(subject, message_body):
    """Send an email notification"""
    try:
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECIPIENT
        msg['Subject'] = subject
        
        # Add message body
        msg.attach(MIMEText(message_body, 'plain'))
        
        # Connect to the SMTP server and send the email
        print(f"Sending email notification to {EMAIL_RECIPIENT}...")
        
        # For Gmail
        if 'gmail' in EMAIL_SMTP_SERVER.lower():
            server = smtplib.SMTP(EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT)
            server.starttls()  # Enable TLS encryption
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            text = msg.as_string()
            server.sendmail(EMAIL_SENDER, EMAIL_RECIPIENT, text)
            server.quit()
        # For Outlook/Hotmail
        elif 'outlook' in EMAIL_SMTP_SERVER.lower() or 'hotmail' in EMAIL_SMTP_SERVER.lower():
            server = smtplib.SMTP(EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT)
            server.starttls()  # Enable TLS encryption
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            text = msg.as_string()
            server.sendmail(EMAIL_SENDER, EMAIL_RECIPIENT, text)
            server.quit()
        # For other email providers
        else:
            server = smtplib.SMTP(EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT)
            server.starttls()  # Enable TLS encryption
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            text = msg.as_string()
            server.sendmail(EMAIL_SENDER, EMAIL_RECIPIENT, text)
            server.quit()
            
        print(f"Email notification sent to {EMAIL_RECIPIENT}")
    except Exception as e:
        print(f"Failed to send email notification: {str(e)}")

def setup_driver():
    """Set up and return a Chrome WebDriver"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    
    # Create and return the WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def scrape_course_info():
    """Scrape the Dal academic timetable website for the course information using Selenium"""
    driver = None
    try:
        print("Starting WebDriver...")
        driver = setup_driver()
        
        # Navigate to the Dal academic timetable
        print(f"Navigating to {URL}...")
        driver.get(URL)
        
        # Wait for page to load initially
        print("Waiting for initial page to load...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "pbid-headerBlock-label"))
        )
        
        # Take a screenshot for debugging
        if not os.path.exists('screenshot_initial.png'):
            driver.save_screenshot('screenshot_initial.png')
            print("Saved initial page screenshot")
        
        # Check if there's a privacy/cookies dialog and handle it
        try:
            privacy_accept = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept')]"))
            )
            privacy_accept.click()
            print("Clicked accept on privacy dialog")
        except TimeoutException:
            print("No privacy dialog found or already accepted")

        # Step 1: Check the appropriate term checkbox (Summer 2024/2025)
        print("Selecting term...")
        try:
            # Uncheck the Winter term if it's selected
            winter_term_checkbox = driver.find_element(By.XPATH, "//input[@id='pbid-termCheckbox-0']")
            winter_term_label = driver.find_element(By.ID, "pbid-termCheckbox-label-0")
            
            if winter_term_checkbox.is_selected():
                winter_term_label.click()
                print(f"Unselected term: {winter_term_label.text}")
                time.sleep(1)  # Wait for page to process

            # Find and select the Summer term (index 1)
            summer_term_checkbox = driver.find_element(By.XPATH, "//input[@id='pbid-termCheckbox-1']")
            summer_term_label = driver.find_element(By.ID, "pbid-termCheckbox-label-1")
            
            if not summer_term_checkbox.is_selected():
                summer_term_label.click()
                print(f"Selected term: {summer_term_label.text}")
                time.sleep(2)  # Wait for page to process term selection
            else:
                print(f"Summer term already selected: {summer_term_label.text}")
                
        except Exception as e:
            print(f"Error selecting term: {str(e)}")
            driver.save_screenshot('error_selecting_term.png')
            print("Saved error screenshot to error_selecting_term.png")

        # Step 2: Verify district selection (default is "All" which is what we want)
        print("Verifying district selection...")
        try:
            district_all_checkbox = driver.find_element(By.ID, "pbid-districtSelectAllCheckbox")
            if not district_all_checkbox.is_selected():
                driver.find_element(By.ID, "pbid-districtSelectAllCheckbox-label").click()
                print("Selected 'All' districts")
                time.sleep(2)  # Wait for page to process district selection
            else:
                print("'All' districts already selected")
        except Exception as e:
            print(f"Error verifying district selection: {str(e)}")

        # Step 3: Wait for subject dropdown to become available
        print("Waiting for subject dropdown to be loaded...")
        try:
            WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.ID, "select2-chosen-1"))
            )
            # Click on the subject dropdown
            driver.find_element(By.ID, "select2-chosen-1").click()
            time.sleep(1)
            
            # Search for the subject in the dropdown
            subject_text = "CSCI"  # Computer Science
            
            print(f"Selecting subject: {subject_text}")
            search_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "select2-input"))
            )
            search_input.clear()
            search_input.send_keys(subject_text)
            time.sleep(2)
            
            # Click on the first matching result
            result = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'select2-result-label')]"))
            )
            result.click()
            print(f"Selected subject in dropdown")
            time.sleep(2)
        except Exception as e:
            print(f"Error selecting subject: {str(e)}")
            # Take a screenshot to see what went wrong
            driver.save_screenshot('error_selecting_subject.png')
            print("Saved error screenshot to error_selecting_subject.png")

        # Step 4: Click the refresh/load button to load the timetable data
        print("Clicking refresh button to load data...")
        try:
            refresh_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "pbid-loadTimetableButton"))
            )
            refresh_button.click()
            print("Clicked refresh button")
            
            # Wait for the loading indicator to appear and then disappear
            try:
                WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, "progressLoader"))
                )
                print("Loading indicator visible, waiting for data...")
                WebDriverWait(driver, 30).until(
                    EC.invisibility_of_element_located((By.CLASS_NAME, "progressLoader"))
                )
                print("Loading completed")
            except TimeoutException:
                print("Warning: Loading indicator not seen or didn't disappear")
                
            # Additional wait to make sure data is fully loaded
            time.sleep(5)
        except Exception as e:
            print(f"Error clicking refresh button: {str(e)}")
            driver.save_screenshot('error_refresh_button.png')
            print("Saved error screenshot to error_refresh_button.png")

        # Step 5: Try finding a filter field and entering the CRN
        print(f"Filtering for CRN: {CRN_TO_MONITOR}")
        try:
            filter_field = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "pbid-filterText"))
            )
            filter_field.clear()
            filter_field.send_keys(CRN_TO_MONITOR)
            time.sleep(3)  # Give time for filtering to apply
            print("Applied filter")
        except Exception as e:
            print(f"Error applying filter: {str(e)}")
        
        # Save final state screenshot for debugging
        driver.save_screenshot('screenshot_final.png')
        print("Saved final state screenshot")
        
        # Save page source for debugging
        with open('page_source_final.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print("Saved final page source")
            
        # Step 6: Look for the CRN in the results table
        print(f"Looking for course with CRN {CRN_TO_MONITOR}...")
        try:
            # Find the table with course data
            table = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "tbodyTimetable"))
            )
            
            # Find all rows in the table
            rows = table.find_elements(By.TAG_NAME, "tr")
            print(f"Found {len(rows)} rows in the table")
            
            # Look for the CRN in each row
            for row in rows:
                row_text = row.text
                if CRN_TO_MONITOR in row_text:
                    print(f"Found CRN {CRN_TO_MONITOR} in row: {row_text}")
                    # Find the availability column
                    cells = row.find_elements(By.TAG_NAME, "td")
                    
                    print(f"Number of cells in row: {len(cells)}")
                    for i, cell in enumerate(cells):
                        print(f"Cell {i}: {cell.text}")
                    
                    if len(cells) > 15:  # Make sure we have enough cells
                        # The "Avail" column is index 15 (based on the terminal output)
                        avail_cell = cells[15]
                        avail_value = avail_cell.text.strip()
                        print(f"Found availability value: {avail_value}")
                        return avail_value
            
            # If we get here, we didn't find the CRN
            print(f"CRN {CRN_TO_MONITOR} not found in table")
            return None
        except Exception as e:
            print(f"Error finding course in table: {str(e)}")
            return None
    
    except Exception as e:
        print(f"Error scraping website: {str(e)}")
        if driver:
            driver.save_screenshot('error_screenshot.png')
            print("Saved error screenshot to error_screenshot.png")
        return None
        
    finally:
        # Always close the WebDriver
        if driver:
            driver.quit()

def check_for_changes():
    """Check for changes in course availability"""
    global CURRENT_VALUE
    
    print(f"{datetime.now()} - Checking for changes in {COURSE_NAME} (CRN: {CRN_TO_MONITOR})...")
    
    new_value = scrape_course_info()
    
    if new_value is None:
        print("Failed to retrieve course information.")
        return
        
    # First run, just store the current value
    if CURRENT_VALUE is None:
        CURRENT_VALUE = new_value
        print(f"Initial value for {VALUE_TO_MONITOR}: {CURRENT_VALUE}")
        return
        
    # Check if the value has changed
    if new_value != CURRENT_VALUE:
        print(f"{VALUE_TO_MONITOR} changed from {CURRENT_VALUE} to {new_value}")
        
        # Prepare notification message
        notification_title = NOTIFICATION_TITLE
        notification_message = f"{COURSE_NAME} ({CRN_TO_MONITOR}): {VALUE_TO_MONITOR} changed from {CURRENT_VALUE} to {new_value}!"
        
        # Send notifications
        send_notification(notification_title, notification_message)
        
        # Update current value
        CURRENT_VALUE = new_value
    else:
        print(f"No change detected. Current {VALUE_TO_MONITOR}: {CURRENT_VALUE}")

def main():
    print(f"Starting Dal Course Monitor for {COURSE_NAME} (CRN: {CRN_TO_MONITOR})")
    print(f"Monitoring {VALUE_TO_MONITOR} value")
    
    # Print notification method
    if EMAIL_ENABLED:
        print(f"Email notifications enabled - will send to {EMAIL_RECIPIENT}")
    
    # Check if running in GitHub Actions
    if os.environ.get('GITHUB_ACTIONS') == 'true':
        print("Running in GitHub Actions - performing a single check")
        check_for_changes()
    else:
        # Only use the continuous loop when running locally
        print(f"Running locally - checking every {CHECK_INTERVAL} seconds")
        print("Press Ctrl+C to stop")
        try:
            while True:
                check_for_changes()
                time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            print("\nMonitor stopped by user.")

if __name__ == "__main__":
    main() 