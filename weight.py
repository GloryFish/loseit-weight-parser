#! /usr/bin/python

#
#  weight.py
#  weight
#
#  Created by Jay Roberts on 2011-06-01
#
#  You can do whatever you want with this. :)
#

import sys
import csv
import datetime
import dateutil.parser
from operator import itemgetter


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

    # load the weight file
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
    weightrows = sorted(weightrows[1:], key=itemgetter(0))  # Remove header line and sort

    weightcsv = None
    weightfile.close()

    # Get the start date from the commandline
    startdate = None
    try:
        startdate = parseDate(sys.argv[2])
    except:
        # Use first date from the csv
        startdate = parseDate(weightrows[0][0])

    # Read weight csv
    weightdata = [(parseDate(row[0]), float(row[1])) for row in weightrows if parseDate(row[0]) >= startdate]

    weightdata = sorted(weightdata, key=lambda row: row[0])

    # Get goal weight from the commandline
    goalweight = None
    try:
        goalweight = int(sys.argv[3])
    except:
        goalweight = None

    log('')

    totaltime = weightdata[-1][0] - startdate
    weeks = int(totaltime.days // 7.0)
    totalloss = weightdata[0][1] - weightdata[-1][1]
    averageloss = totalloss / float(weeks)
    lowweight = min(row[1] for row in weightdata)
    highweight = max(row[1] for row in weightdata)

    # Calculate number of weeks required to hit goal weight
    goaldate = None
    if goalweight is not None:
        tolose = goalweight - weightdata[-1][1]
        weeksleft = tolose / averageloss
        goaldate = datetime.datetime.today() + datetime.timedelta(weeks=weeksleft)

    log('Started on: %d/%d/%d' % (startdate.month, startdate.day, startdate.year))
    log('Starting weight (lbs): %d' % weightdata[0][1])
    log('Highest weight (lbs): %d' % highweight)
    log('Lowest weight (lbs): %d' % lowweight)
    log('Current weight (lbs): %d' % weightdata[-1][1])
    log('Total weight lost (lbs): %d' % totalloss)
    log('# of days: %d' % totaltime.days)
    log('# of weeks: %d' % weeks)
    log('# of months: %d' % int(weeks // 4))
    log('Average lbs/week lost: %.1f' % averageloss)

    if goalweight is not None:
        log('Goal (%dlbs) will be reached on %d/%d/%d' % (goalweight, goaldate.month, goaldate.day, goaldate.year))

    log('')
