#!/usr/bin/python3

import csv

YEAR = "2021"
ALL_DATES_START_TIME = "T000001"

MONTHS = ["Jan", "Feb", "March", "April", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"]

class Entry:
    def __init__(self, date_str, name):
        """
        Create an Entry object from the raw CVS strings.

        Input date_str will be like "Aug 17 - 19" or "April 30 - May 3"

        This object's "dates" will be strings like the DTSTART and DTEND values for the calendar.

        From https://tools.ietf.org/html/rfc5545#page-31,
            FORM #1: DATE WITH LOCAL TIME
                The date with local time form is simply a DATE-TIME value that
                does not contain the UTC designator nor does it reference a time
                zone.  For example, the following represents January 18, 1998, at
                11 PM:
                    19980118T230000
                    YYYYMMDD
                           "T"
                             HHMMSS

        """
        self.date_start = "???"
        self.date_end = "???"
        self.name = name

        parts = date_str.split("-")
        parts0 = parts[0].strip(" ")
        print(f"parts0 = '{parts0}'")
        month0 = parts0.split(" ")[0]
        try:
            iMonth0 = MONTHS.index(month0) + 1
            sMonth0 = str(iMonth0)
            if iMonth0 < 10:
                sMonth0 = "0" + sMonth0
            print(f"MONTH: {month0} = # {iMonth0}")
            self.date_start = YEAR + sMonth0 + "dd" + ALL_DATES_START_TIME
        except ValueError:
            print(f"UNKNOWN MONTH '{month0}'")

        # month 2 may not exist



def parseInputFile(filepath):
    print(f"reading {filepath}....")
    result = []
    with open(filepath, newline='') as csvfile:
        # reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        reader = csv.reader(csvfile)
        for row in reader:
            result.append(row)
    return result


def createVEventString(inputEntry):
    result = ""
    # result = result + "BEGIN:VEVENT\n"
    # result = result + "UID:uid0101@tstdomain.com\n"
    # result = result + "DTSTAMP:19970714T170000Z\n"
    # result = result + "ORGANIZER;CN=Test User:MAILTO:test.user@tstdomain.com\n"
    result = result + "DTSTART:" + inputEntry.date_start + "\n"
    result = result + "DTEND:" + inputEntry.date_end + "\n"
    result = result + "SUMMARY: " + inputEntry.name + "\n"
    # result = result + "GEO:48.85299;2.36885" + "\n"
    result = result + "END:VEVENT\n"
    return result

def printVCalHeader():
    print("BEGIN:VCALENDAR\n")

def printVCalFooter():
    print("END:VCALENDAR\n")


if __name__ == "__main__":
    data = parseInputFile("DCC-in1.csv")
    # print(data)

    printVCalHeader()

    for datum in data:
        event = Entry(datum[0], datum[2])
        # print(f"name: {event.name}, date: {event.date_start}")
        print(f"{createVEventString(event)}")

    printVCalFooter()
