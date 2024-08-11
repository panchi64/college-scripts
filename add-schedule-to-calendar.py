import os
import re
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import filedialog
import icalendar
import pytz
from dateutil import rrule
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager

def get_date_x_weeks_later(date, num_weeks):
    return date + timedelta(weeks=num_weeks)

def days_class_happens(days_input):
    day_map = {
        'L': rrule.MO, 'M': rrule.TU, 'W': rrule.WE,
        'J': rrule.TH, 'V': rrule.FR, 'S': rrule.SA, 'D': rrule.SU
    }
    return [day_map[char] for char in days_input if char in day_map]

def setup_browser():
    print("Setting up Firefox browser...")
    options = webdriver.FirefoxOptions()
    options.add_argument("--start-maximized")
    service = Service(GeckoDriverManager().install())
    return webdriver.Firefox(service=service, options=options)

def login_to_portal(browser):
    print("Navigating to UPRM Portal...")
    browser.get("https://home.uprm.edu/")

    print("Please log in using the opened browser window.")
    print("The script will automatically continue once you're logged in.")

    WebDriverWait(browser, 600).until(ec.url_contains("home.php"))
    print("Login successful!")

def wait_and_click(browser, by, value, timeout=10):
    element = WebDriverWait(browser, timeout).until(
        ec.element_to_be_clickable((by, value))
    )
    try:
        element.click()
    except ElementClickInterceptedException:
        browser.execute_script("arguments[0].click();", element)

def navigate_to_schedule(browser):
    print("Navigating to class schedule...")

    # Navigate to Students Services
    wait_and_click(browser, By.XPATH, "//*[@title='Services for Students']")

    # Navigate to Registration
    wait_and_click(browser, By.XPATH, "//*[@title='Matricula']")

    # Navigate to View Schedule
    wait_and_click(browser, By.CSS_SELECTOR, "a[href*='matricula/appviewmtr.php']")

    # Wait for the schedule to load
    WebDriverWait(browser, 10).until(
        ec.presence_of_element_located((By.CLASS_NAME, "even"))
    )

def get_class_list(browser):
    print("Gathering class details...")
    class_elements = browser.find_elements(By.CLASS_NAME, "even") + browser.find_elements(By.CLASS_NAME, "odd")
    return [element.text for element in class_elements]

def parse_class_info(class_text):
    name = re.search(r"[A-Z]{4}\d{4}", class_text).group()
    prof = re.search(r"\n(.*)\n*(.*)", class_text)
    prof = prof.group().replace("\n", "") if prof else ""
    section = re.search(r"\s\d{3}\w?\s", class_text).group().strip()
    room = re.search(r"[A-Z]+ \d{3}[A-Z]*", class_text)
    room = room.group() if room else "N/A"
    days = re.search(r"\s\s[J-W]{1,5}\s\s", class_text)
    days = days.group().strip() if days else ""
    times = re.findall(r"\d+:\d+\s\w+", class_text)

    if len(times) >= 2:
        s_time = datetime.strptime(times[0], "%I:%M %p").replace(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        e_time = datetime.strptime(times[1], "%I:%M %p").replace(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
    else:
        s_time = e_time = None

    return name, prof, section, room, days, s_time, e_time

def create_calendar(class_list):
    print("Creating calendar...")
    cal = icalendar.Calendar()
    cal.add("version", "2.0")
    cal.add("prodid", "Francisco-Casiano")
    cal.add("calscale", "gregorian")

    tzc = icalendar.Timezone()
    tzc.add('tzid', 'America/Puerto_Rico')
    tzc.add('x-lic-location', 'America/Puerto_Rico')

    tzs = icalendar.TimezoneStandard()
    tzs.add('TZOFFSETFROM', timedelta(hours=-4))
    tzs.add('TZOFFSETTO', timedelta(hours=-4))
    tzs.add('tzname', "AST")
    tzs.add('dtstart', datetime(1970, 1, 1, 0, 0, 0))

    tzc.add_component(tzs)
    cal.add_component(tzc)

    pr_tz = pytz.timezone("America/Puerto_Rico")

    for c in class_list:
        name, prof, section, room, days, s_time, e_time = parse_class_info(c)

        if not all([name, days, s_time, e_time]):
            continue

        event = icalendar.Event()
        event.add("summary", f"{name}-{section}")
        if prof:
            event.add("description", prof)
        event.add("location", room)
        event.add("dtstart", pr_tz.localize(s_time))
        event.add("dtend", pr_tz.localize(e_time))
        event.add("rrule", {
            "freq": "weekly",
            "interval": "1",
            "wkst": "su",
            "until": get_date_x_weeks_later(pr_tz.localize(datetime.now()), 17),
            "byday": days_class_happens(days)
        })
        event.add("status", "CONFIRMED")
        event.add("transp", "OPAQUE")
        event.add("dtstamp", datetime.now())

        cal.add_component(event)

    return cal

def save_calendar(cal):
    print("Saving calendar file...")
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(defaultextension=".ics", filetypes=[("iCalendar", "*.ics")])
    if file_path:
        with open(file_path, "wb") as f:
            f.write(cal.to_ical())
        print(f"Calendar saved to: {file_path}")
    else:
        print("Save operation cancelled.")

def main():
    browser = setup_browser()
    try:
        login_to_portal(browser)
        navigate_to_schedule(browser)
        class_list = get_class_list(browser)
        cal = create_calendar(class_list)
        save_calendar(cal)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Please check if the UPRM portal structure has changed.")
    finally:
        browser.quit()
    print("All done! Have a wonderful day :D")

if __name__ == "__main__":
    main()
