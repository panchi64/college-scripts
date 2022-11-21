# College Scripts

The following sections will describe the details of what each script does and how it works as well as its dependencies. Feel free to use them as you wish if you find any useful 😄.

## Class note setup script _setup-class-note.py_

This script asks the user for a directory on where to create a file. Upon the user choosing where they want their document to be generated, the script will create a Markdown file in that location with the file name being the date and a number using the format `Date-Day-Year(-Index)` (the index is added depending whether there are other files of the same type using the same name already in that location).

### Class note - Dependencies

Use pip install [dependency name] to installed the dependency (if pip doesn't work try using pip3)

- tkinter
- datetime

## Add class schedule to calendar script _add-schedule-to-calendar.py_

This script uses Selenium in order to scrape the UPRM portal website and generate an .ics file containing class' schedules. This file can be imported to any calendar application.

NOTE The application does not gather or store any information other than the courses found, your log-in information is never touched.

(The courses are removed from memory once the application closes, feel free to look at the source code :D)

### Add schedule - Dependencies

Use pip install [dependency name] to installed the dependency (if pip doesn't work try using pip3)

- selenium
- pytz
- os
- icalendar
- datetime
- dateutil
- pathlib
