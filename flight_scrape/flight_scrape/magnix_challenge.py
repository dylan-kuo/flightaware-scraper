import pandas as pd
import os
import matplotlib
matplotlib.style.use('ggplot')
import matplotlib.pyplot as plt
import datetime

pd.set_option('display.max_rows', None)

basePath = os.path.dirname(os.path.abspath(__file__))
df = pd.read_json(basePath + '/flights.json', orient = 'records', dtype={"A":str, "B":list})

print("Total number of rows: ", len(df))

# drop the rows where there's missing value for departure time and arrival time 
df = df[~df['est_arrive_time'].isnull()]
df = df[~df['est_arrive_time'].isnull()]
print("Valid number of rows: ", len(df), "(After preprocessing -- delete missing values)")

# remove all whitespaces
df['departure'] = df['departure'].str.strip()
df['est_arrive_time'] = df['est_arrive_time'].str.strip()

# convert str to datetime format
df['departure'] = pd.to_datetime(df['departure'], format='%a %H:%M%p')
df['est_arrive_time'] = pd.to_datetime(df['est_arrive_time'], format='%a %H:%M%p')

# drop useless parts of datetime (become strtime)
df['departure'] = df['departure'].dt.strftime('%H:%M:%S%p')
df['est_arrive_time'] = df['est_arrive_time'].dt.strftime('%H:%M:%S%p')

# convert back to datetime
df['departure'] = pd.to_datetime(df['departure'])
df['est_arrive_time'] = pd.to_datetime(df['est_arrive_time'])


# ---- 
#departure_time = pd.to_datetime(df['departure'].astype(str)) 
#arrive_time = pd.to_datetime(df['est_arrive_time'].astype(str)) 
# calculate the time flown from departure to arrival in minutes
#df['time_flown'] = arrive_time.sub(departure_time).dt.total_seconds().div(60)
# ----

# calculate time flown in minutes
df['time_flown'] =df['est_arrive_time'].sub(df['departure']).dt.total_seconds().div(60)

# calculate the average time flown per aircrafts (type)
avg_time_flown = df.groupby('type')['time_flown'].mean()
print("\n---- Average Amount of Time Flown ----\n", avg_time_flown)

# --------------------------------------------------------------
# plot for Average Time Flown
avg_time_flown.plot.bar(rot=15, 
                        title="Average Time Flown (minutes)")
plt.show()



# plot for most common airports that these planes flight out from                               

most_common_airports = df.groupby(['origin'])['ident'].count() \
                         .sort_values(ascending=False) \
                         .head(10)
                         
most_common_airports.plot.bar(rot=45,              
                              title="Top 10 Common Airports Flew From",
                              figsize=(12,6))
plt.show()    


# --------------------------------------------------------------
# plof for the most type of aircrafts
most_aircraft_type = df.groupby(['type'])['ident'].count() \
                         .sort_values(ascending=False)                         

bars = plt.bar(most_aircraft_type.index, height=most_aircraft_type.values)
plt.rcParams["figure.figsize"] = (8,6)
# access the bar attributes to place the text in the appropriate location
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + 0.3 , yval + .005, yval)

plt.xlabel('type')
plt.ylabel('Frequency')
plt.title('Most used Aircrafts')
plt.show()

print("\n---- Most Used Aircraft   ----\n", most_aircraft_type)


# --------------------------------------------------------------
# plot for the departure time 

bins = [0,4,8,12,16,20,24]
labels = ['Late Night', 'Early Morning','Morning','Noon','Eve','Night']
#prods = pd.DataFrame({'hour':range(1, 25)})
#prods['session'] = pd.cut(prods['hour'], bins=bins, labels=labels, include_lowest=True)
#print(prods)


def get_hour(x):
    hour = x.strftime('%H')
    hour = int(hour)
    #return datetime.datetime(x.hour)
    return hour

plt.rcParams["figure.figsize"] = (12,8)
df['departure_hour'] = df['departure'].apply(get_hour) 
df['session'] = pd.cut(df['departure_hour'], bins=bins, labels=labels, include_lowest=True)
print(df)


departure_at = df.groupby(['type', 'departure_hour'])['ident'].count() \
                                    .sort_values(ascending=False) \
                                    .unstack(fill_value=0) \
                                    .plot.bar(rot=0, 
                                              title='Most Frequent Departure Hour',                                              
                                              figsize=(12,6))    

# --------------------------------------------------------------
# plot for session
departure_session = df.groupby(['type', 'session'])['ident'].count() \
                                    .sort_values(ascending=False) \
                                    .unstack(fill_value=0) \
                                    .plot.bar(rot=0,
                                              title='Most Frequent Departure Session',
                                              figsize=(12,6))    
                                    
# --------------------------------------------------------------
                                    

