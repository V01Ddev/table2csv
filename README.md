# table2csv

Converts [IAU](https://www.aydin.edu.tr/tr-tr/Pages/default.aspx)'s HTML schedule to a printable CSV and Google calendar CSV

![demo](./demo.gif)

## Usage

This code is meant to be used with [IAU's UBIS](https://ubis.aydin.edu.tr/). Purely made for personal easy of use.

1. Create a virtual environment and run `pip install -r requirement.txt`
1. Run main.py
1. Wait for UBIS to open and login into UBIS
1. return to where the code is running and press enter

`out.csv` is perfect for spreedsheet usage. `GCalender.csv` is meant to be imported into [Google Calender](https://support.google.com/calendar/answer/37118?hl=en).

## In the case that cloudflare is blocking you.

1. Copy the outer html of the `DersProgrami` table.
1. Paste the content into `input.html` at the root of this project.
1. Go to `main.py` and comment out `pull_calender()` in the main function.

This will process the html into the expected outputs.
