import os
import time
import datetime
import argparse
import random
from argparse import ArgumentParser

"""
 Change the date on the file to the specified date.
"""
def change_file_date(file, date):
    # Check if file exists.
    if os.path.isfile(file):
       # Split the date string based on hypens.
       date_split = date.split("-")
       date = datetime.datetime(year  = int(date_split[2]),
                                month = int(date_split[0]),
                                day   = int(date_split[1]),
                                hour  = random.randrange(24),
                                minute = random.randrange(60),
                                second = random.randrange(60) )
       modificationTime = time.mktime(date.timetuple())
       
       # Change the date on the file
       os.utime(file, (modificationTime, modificationTime))
    else:
       print("No such file exists.")
    return

"""
 Check if the date given is an acutal date.
"""
def validate_date(date):
    try:
        datetime.datetime.strptime(date, '%m-%d-%Y')
    except ValueError:
        raise ValueError("Incorrect data format, should be MM-DD-YYYY")

# Main function parse the arguments.
if __name__ == "__main__":
   parser = ArgumentParser()
   parser.add_argument("-f", "--file", dest="filename",
                       help="file to change date")
   parser.add_argument("-d", "--date", dest="date",
                       help="date to change to MM-DD-YYYY format")
   args = parser.parse_args()
   # Validate the date.
   validate_date(args.date)
   change_file_date(args.filename, args.date)
