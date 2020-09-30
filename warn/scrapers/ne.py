import csv
import logging
import requests
import os
import pandas as pd

from bs4 import BeautifulSoup

# spot-check once more

def scrape(output_dir):

    logger = logging.getLogger(__name__)
    output_csv = '{}/nebraska_warn_raw1.csv'.format(output_dir)
    
    years = range(2019, 2009, -1)

    url = 'https://dol.nebraska.gov/LayoffServices/WARNReportData/?year=2020'
    page = requests.get(url)

    logger.info("Page status code is {}".format(page.status_code))
    soup = BeautifulSoup(page.text, 'html.parser')
    table = soup.find_all('table') # output is list-type
  

    # find header
    first_row = table[0].find_all('tr')[2]
    headers = first_row.find_all('th')
    output_header = []
    for header in headers:
        output_header.append(header.text)
    output_header = [x.strip() for x in output_header]

    # save header
    with open(output_csv, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(output_header)

    # save 2020
    output_rows = []
    for table_row in table[0].find_all('tr'):    
        columns = table_row.find_all('td')
        output_row = []
        for column in columns:
            output_row.append(column.text)
        output_row = [x.strip() for x in output_row]
        output_rows.append(output_row)
    output_rows.pop(0) # pop headers
    output_rows.pop(0) # pop headers
    output_rows.pop(0) # pop headers

    if len(output_rows) > 0:
        with open(output_csv, 'a') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(output_rows)


    # save 2019-2010
    for year in years:
        url = 'https://dol.nebraska.gov/LayoffServices/WARNReportData/?year={}'.format(year)

        page = requests.get(url)
        logger.info("Page status code is {}".format(page.status_code))
        soup = BeautifulSoup(page.text, 'html.parser')       
        table = soup.find_all('table') # output is list-type
        
        output_rows = []
        for table_row in table[0].find_all('tr'):    
            columns = table_row.find_all('td')
            output_row = []
            for column in columns:
                output_row.append(column.text)
            output_row = [x.strip() for x in output_row]
            output_rows.append(output_row)
        output_rows.pop(0)
        output_rows.pop(0)
        output_rows.pop(0)

        if len(output_rows) > 0:
            with open(output_csv, 'a') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(output_rows)

    nebraska_two(logger, output_dir)
    combine(logger, output_dir)


def nebraska_two(logger, output_dir):
    
    output_csv = '{}/nebraska_warn_raw2.csv'.format(output_dir)
    years = range(2019, 2009, -1)
    url = 'https://dol.nebraska.gov/LayoffServices/LayoffAndClosureReportData/?year=2020'

    page = requests.get(url)
    logger.info("Page status code is {}".format(page.status_code))
    soup = BeautifulSoup(page.text, 'html.parser')
    table = soup.find_all('table') # output is list-type

    # find header
    first_row = table[0].find_all('tr')[2]
    headers = first_row.find_all('th')
    output_header = []
    for header in headers:
        output_header.append(header.text)
    output_header = [x.strip() for x in output_header]

    # save header
    with open(output_csv, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(output_header)

    # save 2020
    output_rows = []
    for table_row in table[0].find_all('tr'):    
        columns = table_row.find_all('td')
        output_row = []
        for column in columns:
            output_row.append(column.text)
        output_row = [x.strip() for x in output_row]
        output_rows.append(output_row)
    output_rows.pop(0) # pop headers
    output_rows.pop(0) # pop headers
    output_rows.pop(0) # pop headers

    if len(output_rows) > 0:
        with open(output_csv, 'a') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(output_rows)


    # save 2019-2010
    for year in years:

        url = 'https://dol.nebraska.gov/LayoffServices/LayoffAndClosureReportData/?year={}'.format(year)
        page = requests.get(url)
        logger.info("Page status code is {}".format(page.status_code))
        soup = BeautifulSoup(page.text, 'html.parser')
        table = soup.find_all('table') # output is list-type

        output_rows = []
        for table_row in table[0].find_all('tr'):    
            columns = table_row.find_all('td')
            output_row = []
            for column in columns:
                output_row.append(column.text)
            output_row = [x.strip() for x in output_row]
            output_rows.append(output_row)

        output_rows.pop(0)
        output_rows.pop(0)
        if len(output_rows) > 0:
            output_rows.pop(0)

        if len(output_rows) > 0:
            with open(output_csv, 'a') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(output_rows)


def combine(logger, output_dir):

    ne_one = pd.read_csv('{}/nebraska_warn_raw1.csv'.format(output_dir))
    ne_two = pd.read_csv('{}/nebraska_warn_raw2.csv'.format(output_dir))
    ne_all_data = pd.concat([ne_one, ne_two])
    output_csv = '{}/nebraska_warn_raw.csv'.format(output_dir)
    ne_all_data.to_csv(output_csv)
    os.remove('{}/nebraska_warn_raw1.csv'.format(output_dir))
    os.remove('{}/nebraska_warn_raw2.csv'.format(output_dir))

    logger.info("NE successfully scraped.")

if __name__ == '__main__':
    scrape()