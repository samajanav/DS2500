"""
DS2500
Homework 2
Janav Sama
Fall 2023

"""

import csv
import os
import seaborn as sns
import matplotlib.pyplot as plt
import statistics

FILE_DIR = "files"
BIB_HEADER = "BibNumber"
AGE_HEADER = "AgeOnRaceDay"
RANK_HEADER = "RankOverall"
GENDER_HEADER = "Gender"
NAME_HEADER = "FullName"
OFFICIAL_TIME = "OfficialTime"
COUNTRY_ABV = "CountryOfCtzAbbrev"
COUNTRY_RES = "CountryOfResName"

DIRECTORY = "Files/Homework"

def get_filenames(dirname):
    
    """"
    Given a directory name, generate a list of filenames 
    (including the directory as a prefix) for all non-directory files 
    at the top level of the directory.
    """
    filelist = []
    files = os.listdir(dirname)
    for file in files:
        path = dirname + "/" + file
        if not os.path.isdir(path) and not file.startswith("."):
            filelist.append(path)
    return filelist

def read_csv(filename):

    """
    Read the contents of a CSV file given by its filename and return 
    the data as a 2D list, including the header.
    """
    data = []
    with open(filename, "r") as infile:
        csvfile = csv.reader(infile)
        for row in csvfile:
            data.append(row)
    return data
    
def lst_to_dct(lst):
    
    """
    Convert a 2D list into a dictionary, where keys are taken from 
    the header (first row) and values are lists containing 
    corresponding columns from the remaining rows.
    """
    
    header = lst[0]
    dct = {h: [row[i] for row in lst[1:]] for i, h in enumerate(header)}
    return dct

def combine_dcts(lst):
    
    """
    Combine dictionaries from the list 'lst' into a single dictionary 
    'data_dct', favoring values from dictionaries earlier in the list in 
    case of key collisions.
    """

    data_dct = {}
    
    curr_dct = lst_to_dct(lst)
    data_dct = {**data_dct, **curr_dct}
    
    return data_dct

def convert_to_int(lst):
    
    """   
    Convert a list of elements to integers and return the resulting list.
    """

    lst = [int(i) for i in lst]
    
    return lst

def find_mean(lst):
    
    """
    Calculate the mean (average) of a list of numeric values and 
    return the result.
    """
    
    mean_val = statistics.mean(lst)
    
    return mean_val

def find_median(lst):
    
    """
    Calculate the median (middle value) of a list of numeric values and 
    return the result.
    """
    
    median_val = statistics.median(lst)
    
    return median_val

# Homework functions

def get_sec(lst):
    
    """
    Convert a list of time strings in the format 'hh:mm:ss' to a list
    of equivalent seconds. 
    """
    
    time_sec = [int(h) * 3600 + int(m) * 60 + int(s) for h, m, s in 
                (x.split(':') for x in lst)]
    return time_sec


def change_format(integer):
    
    """
    Convert a number of seconds (integer) into hours, minutes,
    and seconds, and return the result as a formatted string. 
    """
    
    mm, ss = divmod(integer, 60)
    hh, mm= divmod(mm, 60)
    
    return "Hours:", hh, "Minutes", mm, "Seconds", ss


def correlation_data (dct,year_values,header, condition):
    
    """
    Calculate the mean of "OfficialTime" values for a specific condition
    in a dictionary (dct) for a list of years (year_values) and return 
    the result as a list of mean values.
    """      
    time_per_data = {}
    mean_data = []
    
    for year in year_values:
        time_per_data[year] = {
            OFFICIAL_TIME: dct[year]["OfficialTime"],
            header: dct[year][header]}
    
    for year in year_values:
        condition_value = []
        for i in range(len(time_per_data[year][header])):
            if time_per_data[year][header][i] == condition:
                condition_value.append(time_per_data[year]
                                       ["OfficialTime"][i])
        stat = statistics.mean(get_sec(condition_value))
        mean_data.append(stat)    
    mean_data = [float(i) for i in mean_data]
 
    return mean_data

def prediction(x,y, x_value):
    
    """
    Perform linear regression on the given data points (x and y) to 
    predict a value at x_value and return the result
    """
    slope, intercept = statistics.linear_regression(x,y)
    value = slope * x_value + intercept 
    
    return value

def normalize(lst):
    
    """
    Normalize a list (lst) by scaling its values to the range [0, 1] 
    based on the minimum and maximum values, and 
    return the normalized version.
    """
    
    norm = []
    mn = min(lst)
    mx = max(lst)
    for x in lst:
        n = (x - mn) / (mx - mn)
        norm.append(n)
    return norm


def main():
    
    # gather data - generate a list of files and read in each one
    # creating a giant dictionary to keep everything in
    # where header = key, value = column under that header
    
    files = get_filenames(DIRECTORY)
    data_dct = {}
    
    for file in files:
        pos = file.find("20")
        year = file[pos:pos+4]
        data = read_csv(file)
        data = combine_dcts(data)
        data_dct[int(year)] = data
    
    year_values = []   
  
    for file in files:
        pos = file.find("20")
        year = (file[pos:pos+4])
        year_values.append(int(year))
    
      
    # Part 1 
    
    # Question 1
    
    time = data_dct[2013][OFFICIAL_TIME]     
    time_in_seonds = get_sec(time) 
    mean_time = find_mean(time_in_seonds)
    print("Question 1:",change_format(mean_time))
    
    # Question 2
    
    age_2010 = data_dct[2010][AGE_HEADER]
    median_age_2010 = find_median(((convert_to_int(age_2010))))
    print("Question 2:",median_age_2010)
    
    # Question 3
    
    country_data = data_dct[2023][COUNTRY_ABV]
    country_data = [value for value in country_data if value != "USA"]
    country_max = statistics.multimode(country_data)
    print("Question 3:",country_max)

    # Question 4
    
    gender_data = data_dct[2021][GENDER_HEADER]
    women_data_2021 = [gender for gender in gender_data if gender == "F"]
    print("Question 3:", len(women_data_2021))
    
    # Question 5
    
    correlation_input = correlation_data(data_dct, year_values, 
                                         GENDER_HEADER, "F")
    correlation_women = round(statistics.correlation(correlation_input, 
                                                     year_values), 4)
    print("Question 5:", correlation_women)

    # Question 6
    
    correlation_input = correlation_data(data_dct, year_values, COUNTRY_RES,
                                         "United States of America")
    correlation_american = round(statistics.correlation(correlation_input,
                                                        year_values), 4)
    print("Question 6:", correlation_american)

    # Question 7
    
    mean_run_data = correlation_data(data_dct,year_values,COUNTRY_RES,
                                      "United States of America")
    mean_2020 = prediction(year_values,mean_run_data,2020)
    
    print("Question 7:",change_format(mean_2020))
 
    
    # Part 2
    
    # Plot 1: Linear Regression
    
    mean_run_data = correlation_data(data_dct,year_values,COUNTRY_RES,
                                      "United States of America")
    # Plotting with details
    
    sns.regplot(x=year_values,y=mean_run_data, label = "Mean Finished Time")
    plt.xlabel("Year")
    plt.ylabel("Americans' Mean Finish Time")
    plt.title("Linear Regression Plot for Mean Finish Time")
    plt.legend()
    plt.show()
     
    # Plot 2: Line Chart
    
    time_per_data = {}
    mean_total_run = []
    age_median = []
    
    # Calculating the median age values and mean time values
    
    for year in year_values:
        age_values = []
        for i in range(len(data_dct[year][AGE_HEADER])):
                age_values.append(data_dct[year][AGE_HEADER][i])
        age_median.append(statistics.median((convert_to_int(age_values))))
 
        run_values = []
        for i in range(len(data_dct[year][OFFICIAL_TIME])):
            run_values.append(data_dct[year][OFFICIAL_TIME][i])
        mean_total_run.append(statistics.mean(get_sec(run_values)))

    # Normalising the values
    
    norm_age = normalize(age_median)
    norm_run = normalize(mean_total_run)
    
    # Creating a line chart with details
    
    sns.lineplot(x=year_values, y=norm_run, marker = "o",
                 label='Average Finish Time')
    sns.lineplot(x=year_values, y=norm_age, marker = "o",label='Median Age')
    sns.despine()
    
    plt.xlabel("Year")
    plt.ylabel("Finish time and age values (normalized)")
    plt.title("Change of finish time and age over the years")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()