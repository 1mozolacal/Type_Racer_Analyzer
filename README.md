# Type Racer Analyzer
This is a combination of python script to scrap your type racer history and display it in a meaningful way.

## How to setup
- You require Python 3 (preferablY 3.8.3+)
- Download packages `pip install beautifulsoup4 requests python-dotenv seaborn`
- Add your username to .env file (replace 'myname' with your name)
- run run.py with `python run.py`
- Go into run.py to change which graph is displayed
- re-run run.py to see changes

When you get the hang of it look at visualizer.py for other types of graphes that you can make. If you want additional functionality either open an issue or make the changes yourself and open a PR.

## Examples

![month line with CI](https://github.com/1mozolacal/Type_Racer_Analyzer/blob/main/media/monthly.png?raw=true)
![WPM and Accuracy vs ID](https://github.com/1mozolacal/Type_Racer_Analyzer/blob/main/media/ful_id.png?raw=true)

## Enhancements
Some possible enhancements I might add if the demand is there. Open an issue to indicate interest.
- Upsert on data. In other words only pull missing data. Will making fetching your last couple of runs very fast
- Parsing data for each run. The text that you wrote, the speed for individual segments, etc.
- Have today use local timezone instead of UTC time
- Multiple plots 


## Packages
pip install beautifulsoup4 requests python-dotenv seaborn

Downloarder Specific:
pip install beautifulsoup4 requests python-dotenv

Visualizer Specific:
pip install seaborn

Developed with Python 3.8.3

