from dotenv import load_dotenv

# --- built-ins ----
import os

# --- files ---
import src.downloader as downloader

if __name__ == '__main__':
    load_dotenv()

USER_NAME = os.environ.get('NAME')
OUTPUT_FILE = os.environ.get('OUTPUT_FILE')
LOAD_FROM_FILE = os.environ.get('LOAD_FROM_FILE')
SAVE_DATA_TO_FILE = os.environ.get('SAVE_DATA')

downloader.main(user='halo1',load_from_file='f')