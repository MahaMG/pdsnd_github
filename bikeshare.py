import pandas as pd
import numpy as np
import functions as func
from tabulate import tabulate # To display the table completely and not block some of the columns


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
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

    # global variables I need in this program.
    global city
    global month
    global day
    global filter_type

    # get user input for city (chicago, new york city, washington). 
    city = func.city()


    # Get user input for the type of filter she/he want to use.
    # She/He must enter one of these four types or she/he will not be able to complete the program.
    filter_list = ['month', 'day', 'both', 'none']
    while True:
        try:
            filter_type = str(input('Would you like to filter the data by month, day, both, or not at all? type "none"for no time filter\n')).lower()
            if filter_type == 'month':
                month = func.month()
                day = None
                break

            elif filter_type == 'day':
                day = func.day()
                month = None
                break
            
            elif filter_type == 'both':
                month = func.month()
                day = func.day()
                break
            
            elif filter_type == 'none':
                month = None
                day = None
                break

            else:
                print('Please enter the correct filter type.')

        except KeyboardInterrupt:
            print('Incorrect value. This is not an option!.')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    # Loads data for the specified city and filters by month and day if applicable.
    # Returns: df - Pandas DataFrame containing city data filtered by month and day
   
    df = pd.read_csv(CITY_DATA[city])
    # Split the date column into three new columns for use in filtering by day, month, and year.
    if filter_type == 'month':
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['year'] = df['Start Time'].dt.year # extract year from the Start Time column to create an year column
        df['month'] = df['Start Time'].dt.month # extract month from the Start Time column to create an month column
        df = df[df['month'] == month]
    elif filter_type == 'day':
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['year'] = df['Start Time'].dt.year
        df['month'] = df['Start Time'].dt.month
        df['day'] = df['Start Time'].dt.day # extract day from the Start Time column to create an day column
        df = df[df['day'] == day]
    
    return df


def time_stats(df):
    # Displays statistics on the most frequent times of trip.

    print('\nCalculating The Most Frequent Times of trip...\n')

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    df['year'] = df['Start Time'].dt.year # extract year from the Start Time column to create an year column
    df['month'] = df['Start Time'].dt.month # extract month from the Start Time column to create an month column
    df['day'] = df['Start Time'].dt.day # extract month from the Start Time column to create an month column
    df['hour'] = df['Start Time'].dt.hour # extract hour from the Start Time column to create an hour column

    if filter_type == 'both' or filter_type == 'month':
        # Find the most booked and ordered day of the month
        popular_day = df[df.month == month].day.mode()[0]
        # Find the hour the most crowded and frequent in it
        popular_hour = df[df.month == month].hour.mode()[0]
        print('Popular day:',popular_day,', Popular hour:', popular_hour)
    
    elif filter_type == 'day':
        # Find the most booked and ordered hour of the day
        popular_hour = df[df.day == day].hour.mode()[0]
        print('Popular hour:', popular_hour)
    
    elif filter_type == 'none':
        # Find the most booked and ordered hour at all
        popular_hour = df[df.year == 2017].hour.mode()[0]
        print('Popular hour:', popular_hour)
    
    print('-'*40)


def station_stats(df):
    # Displays statistics on the most popular stations and trip.

    print('\nCalculating The Most Popular Stations and Trip...\n')

    # display most commonly used start station
    df['Start Station'] = pd.Series(df['Start Station'])
    popular_start_station = df['Start Station'].mode()[0]

    # display most commonly used end station
    df['End Station'] = pd.Series(df['End Station'])
    popular_end_station = df['End Station'].mode()[0]

    # display most frequent combination of start station and end station trip
    popular_trip = df.groupby(['Start Station','End Station']).size().idxmax()

    print('Most Frequent Start Station:', popular_start_station)
    print('Most Frequent End Station:', popular_end_station)
    print('Most popular trip of start station and end station trip:\n',popular_trip)
    
    print('-'*40)


def trip_duration_stats(df):
    # Displays statistics on the total and average trip duration.

    print('\nCalculating Trip Duration...\n')

    # display total trip time
    total_trip_time = df['Trip Duration'].sum()

    # display avg trip time
    mean_trip_time = df['Trip Duration'].mean()

    print('Total trip time:', total_trip_time)
    print('Avg trip time:', mean_trip_time)

    print('-'*40)


def user_stats(df):
    # Displays statistics on bikeshare users.

    print('\nCalculating User Stats...\n')

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('counts of user types\n', user_types)

    # Display counts of gender
    if city != 'washington':
        user_gender = df['Gender'].value_counts()
        print('counts of gender\n', user_gender)

        # Display most common year of birth
        common_yearbirth = df['Birth Year'].mode()
        print('Most common year of birth', common_yearbirth)

    print('-'*40)


def individual_trip(df):
    # Display five more rows of individual trips from dataframe each time the user says "yes"

    # To order print 5 specific rows each time and also not repeated
    n=0 # n = the beginning of the index number
    m=5 # m = the end of the index number
    while True:
        individual_trip = df.iloc[n:m,:]
        print(tabulate(individual_trip)) # tabulate > To display the table completely
        n+=5
        m+=5
        indivi_data = input("\nWould you like to view individual trip data? 'yes' or 'no'.\n")
        if indivi_data.lower() != 'yes':
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        individual_trip(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
