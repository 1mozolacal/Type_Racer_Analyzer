from dotenv import load_dotenv

# --- built-ins ----
import os

# --- files ---
import src.downloader as downloader
import src.visualizer as visualizer

if __name__ == '__main__':
    load_dotenv()

USER_NAME = os.environ.get('NAME')
OUTPUT_FILE = os.environ.get('OUTPUT_FILE')
LOAD_FROM_FILE = os.environ.get('LOAD_FROM_FILE')
SAVE_DATA_TO_FILE = os.environ.get('SAVE_DATA')

data = downloader.main(user=USER_NAME,
    load_from_file=LOAD_FROM_FILE,
    output_file=OUTPUT_FILE,
    save_data_to_file=SAVE_DATA_TO_FILE)

'''
graph_by_months:
Will graph WPM by month, line graph with 95% CI(confidence interval).
'''
visualizer.graph_by_months(data)

'''
graph_on_ids:
Will graph both WPM and accurary on the same graph but different axis. 
The X-axis will be the race ids. In the form of a scatter plot.
'''
#visualizer.graph_on_ids(data)

'''
graph_wpn_by_race_id:
Will graph WPM vs race id in the form of a scatter plot. 
'''
#visualizer.graph_wpn_by_race_id(data)


#leave this to show the plot
visualizer.show()