#! /usr/bin/python

# 
#  weight.py
#  weight
#  
#  Created by Jay Roberts on 2011-06-01.
#  Copyright 2011 DesignHammer. All rights reserved.
# 

import sys
import csv
import datetime
import dateutil.parser

def log(message):
    sys.stdout.write('%s\n' % message)
    sys.stdout.flush()
    
def parseDate(datestring):
    try:
        date = dateutil.parser.parse(datestring)
        return date
    except:
        log('Couldn\'t parse date: %s' % str(datestring))
        return False
    
if __name__ == '__main__':
    # load thr weight file
    filename = None
    try:
        filename = sys.argv[1]
    except:
        log('Please specify a weight csv file.')
        exit()

    weightfile = None
    try:
        weightfile = open(filename, 'r')
    except:
        log('Couldn\'t open file for reading: %s' % filename)
        exit()

    weightcsv = csv.reader(weightfile)
    weightrows = [row for row in weightcsv]
    weightrows = weightrows[1:] # Remove header line
    
    weightcsv = None
    weightfile.close()

    # Get the start date from the commandline
    startdate = None
    try:
        startdate = parseDate(sys.argv[2])
    except:
        startdate = datetime.datetime.today() - datetime.timedelta(weeks=12)

    log('Processing data since %s' % str(startdate))

    # Read weight csv
    weightdata = [(parseDate(row[0]), float(row[1])) for row in weightrows[1:] if parseDate(row[0]) >= startdate]

    weightdata = sorted(weightdata, key=lambda row:row[0])

    for row in weightdata:
        print row



        




# Parse csv

# Calculate:
# - Start date
# - Total time (#of days)
# - Number of weeks
# - Total weight lost
# - Average lbs per week
