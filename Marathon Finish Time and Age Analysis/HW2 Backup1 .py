#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 14:19:17 2023

@author: janavsama
"""

"""
Homework 2
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
    ''' given a directory name, generate all the non-dir filenames
        at the top level and return them as a list of strings, 
        including the directory as a prefix
    '''
    filelist = []
    files = os.listdir(dirname)
    for file in files:
        path = dirname + "/" + file
        if not os.path.isdir(path) and not file.startswith("."):
            filelist.append(path)
    return filelist

def read_csv(filename):
    ''' given the name of a csv file, return its contents as a 2d list,
        including the header.'''
    data = []
    with open(filename, "r") as infile:
        csvfile = csv.reader(infile)
        for row in csvfile:
            data.append(row)
    return data
    

def lst_to_dct(lst):
    ''' given a 2d list, create and return a dictionary.
        keys of the dictionary come from the header (first
                                                     row)
        , values are corresponding columns, saved as lists
        Ex: [[1, 2, 3], [x, y, z], [a, b, c]]
        should return {1 : [x, a], 2 : [y, b], 3 : [z, c]}
    '''
    dct = {h : [] for h in lst[0]}
    for row in lst[1:]:
        for i in range(len(row)):
            dct[lst[0][i]].append(row[i])
    return dct

def combine_dcts(lst):

    data_dct = {}

    curr_dct = lst_to_dct(lst)
    data_dct = {**data_dct, **curr_dct}
    
    return data_dct

def get_sec(lst):
    
    time_sec = []
        
    for i in range(len(lst)):
        h, m, s = lst[i].split(':')
        time_sec.append(int(h) * 3600 + int(m) * 60 + int(s))
    
    return time_sec

def correlation_data (dct,year_values,header, condition):
        
    time_per_data = {}
    mean_data = []
    
    OFFICIAL_TIME = "OfficialTime"
    
    for year in year_values:
        time_per_data[year] = {
            OFFICIAL_TIME: dct[year][OFFICIAL_TIME],
            header: dct[year][header]}
    
    for year in year_values:
        condition_value = []
        for i in range(len(time_per_data[year][header])):
            if time_per_data[year][header][i] == condition:
                condition_value.append(time_per_data[year][OFFICIAL_TIME][i])
        stat = statistics.mean(get_sec(condition_value))
        mean_data.append(stat)
    
    mean_data = [float(i) for i in mean_data]
    
    return mean_data

def main():
    # gather data - generate a list of files and read in each one
    # create a giant dictionary to keep everything in
    # where header = key, value = column under that header
    
    files = get_filenames(DIRECTORY)
    data_dct = {}
    lsts = []
    
    for file in files:
        idx = file.find("20")
        year = file[idx:idx+4]
        data = read_csv(file)
        data = combine_dcts(data)
        data_dct[year] = data
      
    time = data_dct["2013"][OFFICIAL_TIME]     
    time_se = get_sec(time) 
    mean_time = statistics.mean(time_se)
    print(mean_time)

    seconds = mean_time
    print('Time in Seconds:', seconds)
    
    # get min and seconds first
    mm, ss = divmod(seconds, 60)
    # Get hours
    hh, mm= divmod(mm, 60)
    
    print('Time in Seconds:', hh, 'Hours', mm, 'Minutes', ss, 'Seconds')
    
    age_2010 = data_dct["2010"][AGE_HEADER]
    age_2010 = [int(i) for i in age_2010]
    
    median_age = statistics.median(age_2010)
    print(median_age)
    
    country_data = data_dct["2023"][COUNTRY_ABV]
    country_data = [value for value in country_data if value != "USA"]
    country_max = statistics.multimode(country_data)
    print(country_max)

    
    gender_data = data_dct["2021"][GENDER_HEADER]
    women_data_2021 = []
    
    for i in range(len(gender_data)):
        if gender_data[i] == "F":
            women_data_2021.append(gender_data[i])
    print(len(women_data))
    
    # Part 1 - Question 5
    
    # year_values = []   
    # women_data = []
    # time_per_year = {}
    # time_sec_values= []
    # women_mean_time = []
    
    # for file in files:
    #     idx = file.find("20")
    #     year = (file[idx:idx+4])
    #     year_values.append(year) 
  

    # for year in year_values:
    #     time_per_year[year] = {
    #         OFFICIAL_TIME: data_dct[year][OFFICIAL_TIME],
    #         GENDER_HEADER: data_dct[year][GENDER_HEADER]
    # }
    
    # for year in year_values:
    #     a = []
    #     for i in range(len(time_per_year[year][GENDER_HEADER])):
    #         if time_per_year[year][GENDER_HEADER][i] == "F":
    #             a.append(time_per_year[year][OFFICIAL_TIME][i])
    #     stat = statistics.mean(get_sec(a))
    #     women_data.append(stat)
    
    # women_data = [float(i) for i in women_data]
    # year_values = [int(i) for i in year_values]
    
    # correlation_women = statistics.correlation(women_data, year_values)
    # correlation_women = round(correlation_women, 4)
    # print(correlation_women)
    
    
    # Part 1 - Question 5
    
    year_values = []   
  
    for file in files:
        idx = file.find("20")
        year = (file[idx:idx+4])
        year_values.append(year) 
  
    
    correlation_input = correlation_data(data_dct,year_values,GENDER_HEADER,"F")
    year_values = [int(i) for i in year_values]
    
    correlation_women = statistics.correlation(correlation_input, year_values)
    correlation_women = round(correlation_women, 4)
    print(correlation_women)
 
    # Part 1 - Question 6
    
    year_values = []   
  
    for file in files:
        idx = file.find("20")
        year = (file[idx:idx+4])
        year_values.append(year) 
  
    
    correlation_input = correlation_data(data_dct,year_values,COUNTRY_RES,"United States of America")

    year_values = [int(i) for i in year_values]
    
    correlation_american = statistics.correlation(correlation_input, year_values)
    correlation_american = round(correlation_american, 4)
    print(correlation_american)
 

if __name__ == "__main__":
    main()
