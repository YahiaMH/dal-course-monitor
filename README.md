# Dalhousie Academic Timetable Monitor

A Python application that monitors Dalhousie University's academic timetable website for changes in course availability and sends desktop notifications when changes are detected.

## Features

- Monitors specific course CRN for changes in availability
- Checks the website at configurable intervals
- Sends desktop notifications when changes are detected
- Works with the Dalhousie academic timetable website

## Requirements

- Python 3.6+
- Chrome browser (for the Selenium-based monitor)

## Installation

1. Clone or download this repository
2. Install the required packages:

```bash
pip install requests beautifulsoup4 plyer selenium webdriver-manager
```

## Configuration

Edit the `config.py` file to customize:

- The course CRN you want to monitor
- The course name for notifications
- What value to monitor (e.g., "Avail" seats, "WtLst" spots)
- How often to check for changes
- Notification settings

```python
# Example configuration
CRN_TO_MONITOR = "12345"  # Replace with your course CRN
COURSE_NAME = "CSCI 1100"  # Replace with your course name
VALUE_TO_MONITOR = "Avail"  # Monitor available seats
CHECK_INTERVAL = 300  # Check every 5 minutes
```

## Usage

There are two versions of the monitor:

### Basic Monitor (may not work with JavaScript-heavy websites)

```bash
python course_monitor.py
```

### Advanced Monitor (recommended for most users)

This version uses Selenium to handle JavaScript-rendered content:

```bash
python advanced_monitor.py
```

The first time the program runs, it will:
1. Save a screenshot of the website for debugging
2. Save the HTML source for inspection
3. Print available column headers to help with configuration

Keep the program running to continue monitoring. Press Ctrl+C to stop.

## Troubleshooting

If the monitor can't find your course:

1. Check that you entered the correct CRN in `config.py`
2. Examine the `screenshot.png` and `page_source.html` files to understand the website structure
3. Modify the script as needed to navigate the website correctly (e.g., selecting terms, subjects)

## Advanced Customization

The Selenium-based monitor may need additional customization to work with the Dal website, specifically:

1. Navigating to the correct term
2. Selecting the subject
3. Clicking search buttons

These steps will depend on the exact structure of the website and may require editing the `advanced_monitor.py` file.

## License

This project is open source and available under the MIT License. 