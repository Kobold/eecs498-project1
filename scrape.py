from BeautifulSoup import BeautifulSoup
import csv
import os
import re

DIGITS = re.compile(r'\d+')
COUNTY = re.compile(r'\((.+?)\s+County\s*\)')


def extract_data(f):
    """Converts HTML file into iterator of (date, county) tuples."""
    soup = BeautifulSoup(f)
    items = soup.findAll('tr', {'class': 'list_items'})
    for i in items:
        row = [x.contents[0] for x in i.childGenerator()]
        month, day, year, location = row[1:-1]
        yield (month + ' ' + DIGITS.findall(day)[0] + ' '+ year,
               COUNTY.findall(location)[0])


filenames = [
    'html/2004.html',
    'html/2005.html',
    'html/2006.html',
    'html/2007.html',
    'html/2008.html',
    'html/2009.html']

writer = csv.writer(open('crashes.csv', 'wb'))
for filename in filenames:
    print 'opening ' + filename
    f = file(filename)
    for line in extract_data(f):
        writer.writerow(line)
