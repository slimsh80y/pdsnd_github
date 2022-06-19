from importlib.resources import read_binary
import time
from nbformat import read
import datetime as dt
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    while True:
        city = input("In which city chicago, new york city, or washington: ").lower()
        if city not in CITY_DATA.keys():
            print ("Error! this city in not available")
            continue
        else:
            break
        

    # get user input for month (all, january, february, ... , june)
    
    while True:
        month = input("\nWhich month are you going to filter by? You can select any month from january thorough june or select all of them.\n").lower()
        if month not in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
            print("Im sorry, try again, I didn't get that.") 
            continue
        else:
            break


    # get user input for day of week (all, monday, tuesday, ... sunday)
    
    day =  input('Which day of the week would you like to select? Chose a specific day or input all to display data of all days.\n').lower()

    while(True):
        if(day == 'monday' or day == 'tuesday' or day == 'wednesday' or day == 'thursday' or day == 'friday' or day == 'saturday' or day == 'sunday' or day == 'all'):
            break
        else:
            day = input('Day not found, please input correct day: ').lower()


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    
    
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    month = month.lower()
    day = day.title()

    # load data file into a dataframe
    
    df = pd.read_csv(CITY_DATA[city])


    # convert the Start Time column to datetime
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    
    # filter by month if applicable
    
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        
        df = df.query("month == @month")

    # filter by day of week if applicable
    
    if day != 'All':
        
        # filter by day of week to create the new dataframe
        
        df = df.query("day_of_week == @day")
    
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    months = ['january', 'february', 'march', 'april', 'may', 'june']
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    
    try:
        common_month = months[df['month'].mode()[0]-1]
        print('Most common month is: {}'.format(common_month.title()))
    except KeyError:
        print("\nNo data available for this month.")

    # display the most common day of week
    
    try:
        common_day = df['day_of_week'].mode()[0]
        print('Most common day is: {}'.format(common_day))
    except KeyError:
        print("\nNo data available for this day.")

    # display the most common start hour
    
    try:
        common_hour = df['Start Time'].dt.hour.mode()[0]
        print('Most common start hour of day is: {}'.format(common_hour))
    except KeyError:
        print("\nNo data available for this hour.")    
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()


    # display most commonly used start station
    
    common_start_station = df['Start Station'].mode()[0]
    print('Most common start station is: {}'.format(common_start_station))

    # display most commonly used end station
    
    common_end_station = df['End Station'].mode()[0]
    print('Most common end station is: {}'.format(common_end_station))


    # display most frequent combination of start station and end station trip
    
    common_start_end_stations = (df['Start Station'] + ' to ' + df['End Station']).mode()
    print('Most frequent combination of start station and end station trip is: {}'
          .format(common_start_end_stations))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time = {}'.format(total_travel_time))


    # display mean travel time
    
    avg_travel_time = df['Trip Duration'].sum()
    print('Average Travel Time = {}'.format(avg_travel_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    
    user_types = df['User Type'].value_counts()
    print("Counts of user types: \n", user_types)


    if city in ('chicago', 'new york city'):
        
        
        # Display counts of gender
        
        gender_count = df['Gender'].dropna(axis=0).value_counts()
        print("Counts of gender: \n", gender_count)


        # Display earliest, most recent, and most common year of birth
        
        earliest_year = df['Birth Year'].dropna(axis=0).min()
        print("Earliest Birth Year is: {}".format(int(earliest_year)))
        recent_year = df['Birth Year'].dropna(axis=0).max()
        print("Recent Birth Year is: {}".format(int(recent_year)))
        common_year = df['Birth Year'].dropna(axis=0).mode()[0]
        print("Most Common Birth Year is: {}".format(int(common_year)))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def raw_data(df):
    view_data = input('Would you like to review individual trip data? Please Enter Yes or No: ').lower()
    if view_data == 'yes':
        while True:
            try:
                num_of_data = int(input('How many trips? Please enter an numerical integer value'))
                break
            except:
                print('Value is not a number. Please try again. \n')
    start_loc = 0
    while view_data == 'yes':
        data = df.loc[start_loc: start_loc+num_of_data]
        print(data.to_dict(orient='records'))
        start_loc += num_of_data
        view_data = input('Do you want to see more? Yes or No: ').lower()
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
if __name__ == '__main__':
    main()
