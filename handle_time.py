import pandas as pd
import math

# compute weekend bool
def set_value(x):
    if x==5 or x==6:
        return True
    else:
        return False
    
def is_weekend(df: pd.DataFrame):
    copy=df.copy()
    copy['open_date']=pd.to_datetime(copy['open_timestamp'], unit='ms')
    df['is_weekend']=copy['open_date'].dt.weekday.apply(set_value)

# compute cyclical days
def cyclical_days(df: pd.DataFrame):
    copy=df.copy()
    copy['open_date']=pd.to_datetime(copy['open_timestamp'], unit='ms')

    days=[]
    copy['day']=copy['open_date'].dt.weekday
    for i in copy['day']:
        days.append(i)

    sin_days=[]
    cos_days=[]

    for i in days:
        sin_days.append(math.sin(2*math.pi*i/7))
        cos_days.append(math.cos(2*math.pi*i/7))

    sin_days_df=pd.DataFrame(sin_days, columns=['sin_days'])
    cos_days_df=pd.DataFrame(cos_days, columns=['cos_days'])

    df['sin_days']=sin_days_df['sin_days']
    df['cos_days']=cos_days_df['cos_days']

# compute cyclical hours
def cyclical_hours(df: pd.DataFrame):
    copy=df.copy()
    copy['open_date']=pd.to_datetime(copy['open_timestamp'], unit='ms')
    copy['open_hour']=copy['open_date'].dt.hour

    hours=[]
    for i in copy['open_hour']:
        hours.append(i)

    sin_hours=[]
    cos_hours=[]
    for i in hours:
        sin_hours.append(math.sin(2*math.pi*i/24))
        cos_hours.append(math.cos(2*math.pi*i/24))

    sin_hours_df=pd.DataFrame(sin_hours, columns=['sin_hours'])
    cos_hours_df=pd.DataFrame(cos_hours, columns=['cos_hours'])

    df['sin_hours']=sin_hours_df['sin_hours']
    df['cos_hours']=cos_hours_df['cos_hours']