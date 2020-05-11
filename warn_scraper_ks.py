import requests
from bs4 import BeautifulSoup
import gzip
import re

from os import path

import csv 
from datetime import datetime

from bs4 import NavigableString
import os
import requests
import json
import pandas as pd
import re

# spot-checked and linked-checked
# scraper looks good

def kansas():
    
    output_csv = '/Users/dilcia_mercedes/Big_Local_News/prog/WARN/data/kansas_warn_raw.csv'
    max_entries = 950 # manually inserted
    # script should be checked periodically to make sure the entries are below 550 - otherwise, there will be missing info
    start_row_list = range(1, max_entries, 25)

    # Load for first time => get header
    start_row = 1
    # url = 'https://okjobmatch.com/ada/mn_warn_dsp.cfm?securitysys=on&start_row={}&max_rows=50&orderby=employer&choice=1'.format(start_row)
    url = 'https://www.kansasworks.com/ada/mn_warn_dsp.cfm?securitysys=on&start_row={}&max_rows=25&orderby=employer&choice=1'.format(start_row)
    page = requests.get(url)

    print(page.status_code) # should be 200

    soup = BeautifulSoup(page.text, 'html.parser')

    table = soup.find_all('table') # output is list-type
    len(table)

    # find header
    first_row = table[1].find_all('tr')[0]
    headers = first_row.find_all('th')
    output_header = []
    for header in headers:
        output_header.append(header.text)
    output_header = [x.strip() for x in output_header]
    output_header

    # save header
    with open(output_csv, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(output_header)

    for start_row in start_row_list:
        try:
            url = 'https://www.kansasworks.com/ada/mn_warn_dsp.cfm?securitysys=on&start_row={}&max_rows=25&orderby=employer&choice=1'.format(start_row)

            page = requests.get(url)

            print(page.status_code) # should be 200

            soup = BeautifulSoup(page.text, 'html.parser')

            table = soup.find_all('table') # output is list-type

            output_rows = []
            for table_row in table[1].find_all('tr'):    
                columns = table_row.find_all('td')
                output_row = []
                for column in columns:
                    output_row.append(column.text)
                output_row = [x.strip() for x in output_row]
                output_rows.append(output_row)
            output_rows.pop(0)
            output_rows.pop(0)
            print(output_rows[0])

            with open(output_csv, 'a') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(output_rows)

        except IndexError:
            print(url + ' not found')


if __name__ == '__main__':
    kansas()