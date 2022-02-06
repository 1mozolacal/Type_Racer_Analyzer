import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# --- built-ins ---
import os
import copy
import csv
import time
import datetime

if __name__ == '__main__':
    load_dotenv()
USER_NAME = os.environ.get('NAME')
OUTPUT_FILE = os.environ.get('OUTPUT_FILE') or 'typeracer_data.csv'
LOAD_FROM_FILE = os.environ.get('LOAD_FROM_FILE') or 'true'
SAVE_DATA_TO_FILE = os.environ.get('SAVE_DATA') or 'true'

def get_page(user_name,start_date='',universe='',cursor=None):
    number_per_page = 100
    base_url = "https://data.typeracer.com/pit/race_history"
    url = f"{base_url}?user={user_name}&n={number_per_page}&startDate={start_date}&universe={universe}" if cursor is None else f"{base_url}{cursor}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    rows = soup.find_all(class_="Scores__Table__Row")
    next_page = soup.find("a",string="\n          load older results »\n        ")
    next_page = None if next_page is None else next_page['href']

    data = []
    for row in rows:
        race_id_link,wpm,accuracy,points,placement,date,_ghost = get_children_tags(row)
        row_data = (get_children_tags(race_id_link)[0]['href'],
            str(wpm.string),
            str(accuracy.string),
            str(points.string),
            str(placement.string),
            str(date.string))#len 6
        data.append(row_data)
    return (data,next_page)

def get_children_tags(parent):
    return [x for x in parent.contents if not x == '\n']

def get_soup(user_name):
    start_time = time.time()
    batch_time = time.time()
    cursor = None
    first_run = True
    data = []
    while not cursor is None or first_run:
        first_run = False
        rows, cursor = get_page(user_name,cursor=cursor)
        data.extend(rows)
        print(f'fetched data, batch took {round(time.time()-batch_time,1)}s. Currently at {len(data)} records in {round(time.time()-start_time,1)}s')
        batch_time = time.time()
        time.sleep(5)
    return data

def clean_up_soup(data):
    # Raw data looks like:
    #   race_id_link,wpm,accuracy,points,placement,date

    no_white = [[item.strip() for item in row] for row in data]
    clean_data = []
    for row in no_white:
        run_id = int(row[0].split('|')[-1])
        clean_row = (run_id,
            row[0],
            row[1].replace(' WPM',''),
            float(row[2].replace('%','')),
            0 if row[3] == 'N/A' else int(row[3]),
            row[4],
            get_standard_date(row[5]))
        clean_data.append(clean_row)
    clean_data = sorted(clean_data,key= lambda x: x[0])
    return clean_data

def get_standard_date(input_date):
    if input_date == 'today':
        date = datetime.datetime.utcnow()
        return date.strftime('%Y-%m-%d')
    month,day,year = input_date.split(' ')
    year = int(year)
    day = int(day.replace(',',''))
    temp_month = datetime.datetime.strptime(month[:3],"%b")
    month = temp_month.month
    date = datetime.datetime(year, month, day)
    return date.strftime('%Y-%m-%d')


def load_data_from_file(output_location):
    data = None
    with open(output_location,'r') as read_file:
        csv_reader = csv.reader(read_file)
        data = [x for x in csv_reader][1:]# peal off header
    return data

def load_data_from_site(user):
    raw_data = get_soup(user)
    data = clean_up_soup(raw_data)
    return data

def save_to_file(DATA,output_location):
    header = ("id","info_link","WPM","accuracy","points","placement","date")
    data = copy.deepcopy(DATA)
    data.insert(0,header)
    with open(output_location,"w+", newline='') as output_file:
        csv_writer = csv.writer(output_file)
        csv_writer.writerows(data)

def main(
    user=USER_NAME,
    output_file=OUTPUT_FILE,
    load_from_file=LOAD_FROM_FILE,
    save_data_to_file=SAVE_DATA_TO_FILE):
    has_file = os.path.isfile(output_file)
    if user is None:
        print("Warning missing username, this is required if you are pulling data")
        if not(has_file and not save_data_to_file is None 
            and not save_data_to_file.lower() in ['false','f']):
            exit()
    output_file = output_file or 'typeracer_data.csv'
    load_from_file = load_from_file or 'true'
    save_data_to_file = save_data_to_file or 'true'
    
    working_dataset = []

    if load_from_file and has_file and not load_from_file.lower() in ['false','f']:
        print("reading from file")
        working_dataset = load_data_from_file(output_file)
        #TODO - perform upsert here
    else:
        print("reading from site")
        working_dataset = load_data_from_site(user)
        if not save_data_to_file.lower() in ['false','f']:
            save_to_file(working_dataset,output_file)
    
    return working_dataset

if __name__ == '__main__':
    main()