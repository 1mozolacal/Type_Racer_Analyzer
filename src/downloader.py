import requests
from bs4 import BeautifulSoup

# --- built in ----
import os

USER_NAME = os.environ.get('NAME') or 'halo1' 
OUTPUT_FILE = os.environ.get('OUTPUT_FILE') or 'typeracer_data.csv'
LOAD_FROM_FILE = os.environ.get('LOAD_FROM_FILE') or 'true'

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
    cursor = None
    first_run = True
    data = []
    while first_run:#not cursor is None or first_run:
        first_run = False
        print(f'fetching data {len(data)} at cursor {cursor}')
        rows, cursor = get_page(user_name)
        data.extend(rows)
    return data

def clean_up_soup(data):
    # Raw data looks like:
    # race_id_link,wpm,accuracy,points,placement,date

    no_white = [[item.strip() for item in row] for row in data]
    clean_data = []
    for row in no_white:
        run_id = int(row[0].split('|')[-1])
        date = row[5]
        if date in ['today']:
            pass #TODO
        clean_row = (run_id,
            row[0],
            row[1].replace(' WPM',''),
            float(row[2].replace('%','')),
            int(row[3]),
            row[4],
            date)
        clean_data.append(clean_row)
    return clean_data

def load_data_from_file():
    pass

get_soup('halo1')


def main():
    has_file = os.path.isfile(OUTPUT_FILE)
    working_dataset = []

    if LOAD_FROM_FILE and has_file:
        working_dataset = load_data_from_file()
    else:
        pass

if __name__ == '__main__':
    main()