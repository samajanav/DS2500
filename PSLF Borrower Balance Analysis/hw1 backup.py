#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 14:14:45 2023

@author: janavsama
"""

import csv
import matplotlib.pyplot as plt

BORROWERS_LIST = "pslf_borrowers.csv"
BALANCE_LIST = "pslf_balance.csv"

def read_csv(filename, skip_rows = 1):
    
    ''' read the given CSV into a 2d list of strings and return it.
        Skips the first skip_rows as headers, and keeps only the first
        keep_cols of each rows.
    '''

    borrowers = []
    with open(filename, "r") as infile:
        csvfile = csv.reader(infile)
        for i in range(skip_rows):
            next(csvfile)
        for row in csvfile:
            borrowers.append(row)
    return borrowers

def str_to_float(string):
    ''' Given a string with possible extra characters (, $)
        remove the extra characters and convert/return
        the string as a float
    '''
    stripped_data = string.replace(",", "")
    stripped_data = stripped_data.replace("$", "")

    return float(stripped_data)

def twod_to_dct(lst):
    ''' Given a 2d list of structure [[x, y, ..., z], [x, y, ..., z]]
        create and return a dictionary where the first element
        of every row becomes a key, rest of row is the value
    '''
    dct = {}
    for item in lst:
        key = item[0]
        value = [(i) for i in item[1:]]
        dct[key] = value
    return dct

#Homework function 

def total(lst):
    
    total_sum = 0
    
    for i in range(len(lst)):
        total = (lst[i])
        for sublist in total:
            for value in sublist:
                total_sum += value
    return total_sum

def state_difference(dct):

    may = []
    march = []
    total_diff = []
    
    for i in range(len(dct)):
        may.append(int(dct[i][0]))
        march.append(int(dct[i][10]))
        
    for i in range(len(dct)):
        total_diff.append(march[i] - may[i])
    return total_diff

def balance_increase(state,state_names,dct):
    
    average = 0
    input_average = []
    state_pos = state_names.index(state)
    input_value = dct[state_pos]
    input_state = []
    
    for i in range(1,len(input_value)):
       average = input_value[i]-input_value[i-1]
       input_average.append(average)
    input_average = sum(input_average) / len(input_value)
        
    return input_average

def average_outstanding_balance(dct):
    
    values_stored = []
    
    for i in range(len(dct)):
        values_stored.append(dct[i][6])  
    return values_stored

def outstanding_balance_line(dct,pos):
    
    values_stored = []

    for i in range(len(dct)):
        row_values = []
        for j in range(len(dct[i])):
            row_values.append(dct[pos][j])
            values_stored.append(row_values)
        
    return row_values
        

def main():
    # gather data - read from the csv file into a 2d list
    borrowers = read_csv(BORROWERS_LIST, skip_rows = 1)
    balance = read_csv(BALANCE_LIST, skip_rows = 1)
    

    # clean up the borrowers data
    data_borrowers = twod_to_dct(borrowers)
    
    # clean up for balance data
    
    state_names = []
    state_balance_values = []
    strip_data = []
    
    for i in range(len(balance)):
        state_names.append(balance[i][0])
    for row in balance:
        state_balance_values.append(row[1:])
        
    for i in range(len(state_balance_values)):
        row_values = []
        for j in range(len(state_balance_values[i])):
            row_values.append(str_to_float(state_balance_values[i][j]))
        strip_data.append(row_values)
            
    # cleaned_balance = clean_data(strip_data) 
    # data_balance = twod_to_dct(strip_data)
    
    state_balance_values = []
    strip_balance_data = []
    
    for i in range(len(balance)):
        state_names.append(balance[i][0])
    for row in balance:
        state_balance_values.append(row[1:])
        
    for i in range(len(state_balance_values)):
        row_values = []
        for j in range(len(state_balance_values[i])):
            row_values.append(str_to_float(state_balance_values[i][j]))
        strip_balance_data.append(row_values)
        
    state_borrower_values = []
    strip_borrowers_data = []
    
    for row in borrowers:
        state_borrower_values.append(row[1:])
    
    for i in range(len(state_borrower_values)):
        row_values = []
        for j in range(len(state_borrower_values[i])):
            row_values.append(str_to_float(state_borrower_values[i][j]))
        strip_borrowers_data.append(row_values)
     
    total_1 = state_difference(strip_data)
    highest_value = max(total_1) 
    total_state = total_1.index(highest_value)  
    highest_state = state_names[total_state]    
    # print("Highest state:",highest_state)
    
    total_2 = state_difference(strip_data)
    lowest_value = min(total_2) 
    total_state = total_2.index(lowest_value) 
    highest_state = state_names[total_state]    
    # print("Lowest value:",highest_state)
    
    # input_state = input("What state?")
    # difference = balance_increase(input_state,state_names,strip_data)
    # print(difference)
    
    
    borrowers_nov = average_outstanding_balance(strip_borrowers_data)
    balance_nov = average_outstanding_balance(strip_balance_data)   
    balance_nov = [i * 1000000 for i in balance_nov ]
    average_balance = []
    values_hist = []

    for i in range(len(balance_nov)):
        average_balance.append(balance_nov[i] / borrowers_nov[i])
        pos = average_balance.index(average_balance[i])
        values_hist = average_balance
        

    # plt.figure(figsize=(10, 6))  # Adjust the figure size
    # plt.hist(average_balance, bins=20, color='red')
    # plt.title('Distribution of Average Balance per Borrower in November')
    # plt.xlabel('Average Balance (in millions)')
    # plt.ylabel('Frequency')
    
    # # Add grid lines
    # plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # # Customize the x-axis tick labels
    # plt.xticks(rotation=45)
    
    # plt.show()
    
    ct_borrowers_values = outstanding_balance_line(strip_borrowers_data,pos = 7)
    dl_borrowers_values = outstanding_balance_line(strip_borrowers_data,pos = 7)
       
    ct_balance_values = outstanding_balance_line(strip_balance_data,pos = 6)
    ct_balance_values = [i * 1000000 for i in ct_balance_values ]
    dl_balance_values = outstanding_balance_line(strip_balance_data,pos = 7)
    dl_balance_values = [i * 1000000 for i in dl_balance_values ]
    
    average_balance_1 = []
    values_hist_1 = []
    average_balance_2 = []
    values_hist_2 = []
    

    for i in range(len(ct_balance_values)):
        average_balance_1.append(ct_balance_values[i] / ct_borrowers_values[i])
        pos = average_balance_1.index(average_balance_1[i])
        values_hist_1 = average_balance_1
        
    for i in range(len(dl_balance_values)):
        average_balance_2.append(dl_balance_values[i] / dl_borrowers_values[i])
        pos = average_balance_2.index(average_balance_2[i])
        values_hist_2 = average_balance_2
    
    # plt.plot(values_hist_1,markersize = 12)
    # plt.plot(values_hist_2, markersize = 12)
 
    # total borrowers
    total_borrowers = total(state_borrower_values)
    print(total_borrowers)
    
    # #Total balance
    # total_balance = total(data_balance)
    
    # # Average Balance
    # average_value = total_balance / total_borrowers
    
    
    
if __name__ == "__main__":
    main()