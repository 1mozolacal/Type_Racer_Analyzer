import seaborn as sns
sns.set()
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# data format
#   race_id,race_id_link,wpm,accuracy,points,placement,date
RACE_ID = 0
RACE_ID_LINK = 1
WPM = 2
ACCURACY = 3
POINTS = 4
PLACEMENT = 5
DATE = 6


def graph_wpm_by_date():
    pass

def graph_wpn_by_race_id(raw_data,number_of_points=100):
    average_amount = max(int(len(raw_data)/number_of_points),1)
    ids = [int(item[RACE_ID]) for item in raw_data]
    wpms = [int(item[WPM]) for item in raw_data]
    
    x,y = compress_y_axis(ids,wpms,average_amount)
    data = pd.DataFrame({'id':x,'wpm':y})
    sns.scatterplot(data=data,x='id',y='wpm')

def graph_accuracy_by_race_id(raw_data,number_of_points=100,axis=None):
    average_amount = max(int(len(raw_data)/number_of_points),1)
    ids = [int(item[RACE_ID]) for item in raw_data]
    accuracys = [float(item[ACCURACY]) for item in raw_data]
    
    x,y = compress_y_axis(ids,accuracys,average_amount)
    data = pd.DataFrame({'id':x,'accuracy':y})
    sns.scatterplot(data=data,x='id',y='accuracy',color='r',ax=axis)

def graph_on_ids(raw_data,number_of_points=100):
    graph_wpn_by_race_id(raw_data,number_of_points=number_of_points)
    plt.legend(['WPM'])
    ax2 = plt.twinx()
    graph_accuracy_by_race_id(raw_data,number_of_points=number_of_points,axis=ax2)
    plt.legend(['Accuracy'])
    plt.title("WPM and Accurrcy by race ID")

def compress_y_axis(x,y,group_by):
    temp_x = []
    temp_y = []
    summation = []
    for index,value in enumerate(zip(x,y)):
        x_item,y_item = value
        if index % group_by == 0:
            temp_x.append(x_item)
        summation.append(y_item)
        if index % group_by == group_by-1:
            temp_y.append(sum(summation)/len(summation))
            summation=[]
            
    if not len(x) == len(temp_y):
        temp_y.append(sum(summation)/len(summation)) 
    return (temp_x,temp_y)


def graph_by_months(raw_data,start_date=None):
    #start_data in formate "YYYY-mm-dd"
    dates = [numerize_date(item[DATE],start_date=start_date) for item in raw_data]
    wpms = [int(item[WPM]) for item in raw_data]
    x,y=[],[]
    min_date = min([x for x in dates if not x is None])
    for date,wpm in zip(dates,wpms):
        if date is None:
            continue
        else:
            x.append(date - min_date)
            y.append(wpm)
    data = pd.DataFrame({'date':x,'wpm':y})
    #sns.scatterplot(data=data,x='id',y='wpm')
    sns.lineplot(data=data,x='date',y='wpm')

def numerize_date(date,interval='month',start_date=None):
    year,month,day = date.split('-')
    date_value = 0
    if(interval == 'year'):
        date_value = int(year)
    elif(interval == 'month'):
        date_value = (int(year) * 12) + ( int(month) - 1)
    else:
        return None
    
    if start_date is None:
        return date_value
    else:
        start_date_value = numerize_date(start_date,interval)
        if start_date_value < date_value:
            return date_value
        else:
            return None

def show():
    plt.show()
