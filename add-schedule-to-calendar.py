# To gather the class schedules
import os
# Information parsing
import re
from datetime import datetime, timedelta
# Asking user where to place the created .ics file
from tkinter import Tk
from tkinter import filedialog

import icalendar
# To create and hydrate the ics calendar file
import pytz
from dateutil import rrule
from icalendar import Calendar, Event
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


# Calculate the date x amount of weeks from given date
def get_date_x_weeks_later(date, num_weeks):
    td = timedelta(weeks=num_weeks)
    return date + td


# Uses the parsed day data and produces a string usable by the icalendar library for an event
def days_class_happens(days):
    response = []
    for char in days:
        if char == "L":
            response.append(rrule.MO)
        elif char == "M":
            response.append(rrule.TU)
        elif char == "W":
            response.append(rrule.WE)
        elif char == "J":
            response.append(rrule.TH)
        elif char == "V":
            response.append(rrule.FR)
        elif char == "S":
            response.append(rrule.SA)
        elif char == "D":
            response.append(rrule.SU)
    return response


# Open the old UPRM portal with selenium
print("Downloading Google Chrome for automated usage...")
# TODO: See if there is a way to completely remove all traces of the script running by deleting the chrome driver
#  after script completion.
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

print("Google Chrome installed, launching to Old UPRM Portal")
browser.get("https://home.uprm.edu/")
assert "LOGIN" in browser.title

# Wait for the user to log in (timeout of 10 mins)
print("Please log in...")
WebDriverWait(browser, 600).until(ec.url_contains("home.php"))
assert "My Home" in browser.title

# Direct the user into the schedule page
print("Great! Redirecting you to the class schedule page...")
browser.find_element(by=By.XPATH, value="//*[@title='Services for Students']").click()
assert "Estudiantes" in browser.title

browser.find_element(by=By.XPATH, value="//*[@title='Matricula']").click()
assert "Matrícula" in browser.title

browser.find_element(by=By.CSS_SELECTOR, value="a[href*='matricula/appviewmtr.php']").click()
assert "Clases Matriculadas" in browser.title

# Make a list of all the courses
print("Gathering class details...")
class_elements = browser.find_elements(by=By.CLASS_NAME, value="even")
class_elements += browser.find_elements(by=By.CLASS_NAME, value="odd")

class_list = []
for element in class_elements:
    class_list.append(element.text)

# Ask the user where to place the generated .ics file
print("Class information found, file is ready to be generated. Please select where to place the calendar file:")
try:
    Tk().withdraw()
    parent_dir = filedialog.askdirectory()
except:
    print("Error: Could not get the directory from the given selection.")
    exit()

# Time the class starts and ends
print("Creating file and placing it in " + parent_dir)
pr_tz = pytz.timezone("America/Puerto_Rico")

cal = Calendar()
cal.add("version", "2.0")
cal.add("prodid", "Francisco-Casiano")
cal.add("calscale", "gregorian")

# Setup timezone details for the calendar... For some reason this isn't easily done with the library???
tzc = icalendar.Timezone()
tzc.add('tzid', 'America/Puerto_Rico')
tzc.add('x-lic-location', 'America/Puerto_Rico')

# TODO: Check these lines there may be a logic issue here
tzs = icalendar.TimezoneStandard()
tzs.add('TZOFFSETFROM', timedelta(hours=-4))
tzs.add('TZOFFSETTO', timedelta(hours=-4))
tzs.add('tzname', "AST")
tzs.add('dtstart', datetime(1970, 1, 1, 0, 0, 0))

tzc.add_component(tzs)
cal.add_component(tzc)

uid = 0

# Iterate through the list of classes and create events lasting a semester (17 weeks) for each class on their
# corresponding days
for c in class_list:
    # Parse information
    name = re.search(r"[A-Z]{4}\d{4}", c).group()

    # This circumvents the phantom professor scenario
    try:
        prof = re.search(r"\n(.*)\n*(.*)", c).group()
        prof = prof.replace("\n", "")
    except AttributeError:
        prof = ""

    section = re.search(r"\s\d{3}\s", c).group() if re.search(r"\s\d{3}\s", c) else "N/A"
    section = section.strip()
    room = re.search(r"[A-Z]+ \d{3}[A-Z]*", c).group() if re.search(r"[A-Z]+ \d{3}[A-Z]*", c) else "N/A"
    days = re.search(r"\s\s[J-W]{1,5}\s\s", c).group() if re.search(r"\s\s[J-W]{1,5}\s\s", c) else "N/A"
    days = days.strip()

    time = re.findall(r"\d+:\d+\s\w+", c)
    if len(time) > 0:
        s_time = datetime.strptime(time[0], "%I:%M %p").replace(day=datetime.now().day, year=datetime.now().year,
                                                                month=datetime.now().month)
        e_time = datetime.strptime(time[1], "%I:%M %p").replace(day=datetime.now().day, year=datetime.now().year,
                                                                month=datetime.now().month)

    course = Event()
    course.add("summary", name + "-" + section)
    course.add("description", prof)
    course.add("location", room)

    try:
        s_time
        e_time
    except NameError:
        print("The starting time and ending time for the course was not found, not placing them in the calendar")
    else:
        course.add("dtstart", pr_tz.localize(s_time))
        course.add("dtend", pr_tz.localize(e_time))

    # Recurrence details
    course.add("rrule", {"freq": "weekly", "interval": "1", "wkst": "su",
                         "until": get_date_x_weeks_later(pr_tz.localize(datetime.now()), 17),
                         "byday": days_class_happens(days)})

    course.add("status", "CONFIRMED")
    course.add("transp", "OPAQUE")

    course.add("dtstamp", datetime.now())

    cal.add_component(course)
    uid += 1

# Create .ics file
cal_file = open(os.path.join(parent_dir, "class_schedule.ics"), "wb")
cal_file.write(cal.to_ical())
cal_file.close()

browser.quit()
print("All done! Have a wonderful day :D")
