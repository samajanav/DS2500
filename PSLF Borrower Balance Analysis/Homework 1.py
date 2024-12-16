"""
DS2500
Homework 1
Janav Sama
Fall 2023

"""

import csv
import matplotlib.pyplot as plt

BORROWERS_LIST = "pslf_borrowers.csv"
BALANCE_LIST = "pslf_balance.csv"

def read_csv(filename, skip_rows = 1):
    
    ''' Read the given CSV into a 2d list of strings and return it.
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

# Homework functions 

def total(lst):
    
    """
    Given a nested list of numeric values, the function adds up all the 
    values and returns the total sum.
    
    """
       
    total_sum = 0
    values = []
    
    for i in range(len(lst)):
        values.append(lst[i][10])

    for value in values:
        total_sum += value
    
    return total_sum

def state_difference(dct):
    
    """
    
    Takes a dictionary and calculates the difference between March and May
    values for each entry 
    
    """
    
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
    
    """
    Calculate the average difference between consecutive values for a 
    specific state's data.
    """
    
    input_average = []
    state_pos = state_names.index(state)
    input_value = dct[state_pos]
    
    for i in range(1,len(input_value)):
       average = input_value[i]-input_value[i-1]
       input_average.append(average)
    input_average = sum(input_average) / len(input_average)
        
    return input_average

def average_outstanding_balance(dct):
    
    """
    Calculate the average outstanding balance from a dictionary.
    
    """
    
    values_stored = []
    
    for i in range(len(dct)):
        values_stored.append(dct[i][6])  
    return values_stored

def outstanding_balance_line(dct,pos):
    
    """
    Calculate the average outstanding balance of CT and DL using pos as
    their postion in the list.
    
    """
    
    values_stored = []

    for i in range(len(dct)):
        row_values = []
        for j in range(len(dct[i])):
            row_values.append(dct[pos][j])
            values_stored.append(row_values)
        
    return row_values
        
def avg_balance_state(lst1,lst2):
    
    """
    Calculate the average balance by dividing the balance and borrower data 
    of all months in CT and Dl
    
    """
    average_balance = []
    
    for i in range(len(lst1)):
        average_balance.append(lst1[i] / lst2[i])
        average_balance.index(average_balance[i])
        
    return average_balance

def main():
    
    # gather data - read from the csv file into a 2d list
    borrowers = read_csv(BORROWERS_LIST, skip_rows = 1)
    balance = read_csv(BALANCE_LIST, skip_rows = 1)
    
    # Storing Balance values as floats in strip_balance_data for further
    # calculations
    
    state_balance_values = []
    strip_balance_data = []
    state_names = []
    
    for i in range(len(balance)):
        state_names.append(balance[i][0])
    for row in balance:
        state_balance_values.append(row[1:])
        
    for i in range(len(state_balance_values)):
        row_values = []
        for j in range(len(state_balance_values[i])):
            row_values.append(str_to_float(state_balance_values[i][j]))
        strip_balance_data.append(row_values)
        
    # Storing Borrowers' values as floats in strip_balance_data for further
    # calculations
        
    state_borrower_values = []
    strip_borrowers_data = []
    
    for row in borrowers:
        state_borrower_values.append(row[1:])
    
    for i in range(len(state_borrower_values)):
        row_values = []
        for j in range(len(state_borrower_values[i])):
            row_values.append(str_to_float(state_borrower_values[i][j]))
        strip_borrowers_data.append(row_values)   
        
    # Part 1
    
    # Question 1:  Total_borrowers
    total_borrowers = total(strip_borrowers_data)
    print("Question 1:",total_borrowers)
    
    # Question 2: Total balance
    total_balance = total(strip_balance_data)
    print("Question 2:", total_balance)
    
    # Question 3: Average Balance
    average_value = total_balance * 1000000 / total_borrowers
    print("Question 3:", average_value)
     
    # Question 4-5: Greatest increase in outstanding balance
    total_1 = state_difference(strip_balance_data)
    highest_value = max(total_1) 
    total_state = total_1.index(highest_value)  
    highest_state = state_names[total_state] 
    print("Questions 4-5:")
    print("Highest state:",highest_state)
    print("By how much?:", highest_value)
    
    # Question 6-7: Lowest increase in outstanding balance
    total_2 = state_difference(strip_balance_data)
    lowest_value = min(total_2) 
    total_state = total_2.index(lowest_value) 
    lowest_state = state_names[total_state]   
    print("Questions 6-7:")
    print("Lowest value:",lowest_state)
    print("By how much?:",lowest_value)
    
    # Question 8: Outstanding balance of a given state
    input_state = input("What state?")
    difference = balance_increase(input_state,state_names,strip_balance_data)
    print("Question 8:",difference)
    
    
    # Part 2
    
    # Plot 1: Histogram
    
    borrowers_nov = average_outstanding_balance(strip_borrowers_data)
    balance_nov = average_outstanding_balance(strip_balance_data)   
    balance_nov = [i * 1000000 for i in balance_nov ]
    average_balance = []

    for i in range(len(balance_nov)):
        average_balance.append(balance_nov[i] / borrowers_nov[i])
        average_balance.index(average_balance[i])   

    plt.figure(figsize=(10, 6))
    plt.hist(average_balance, bins=20, color='red',edgecolor='black')
    plt.title('Distribution of Average Balance per Borrower in November')
    plt.xlabel('Average Balance (in millions)')
    plt.ylabel('Frequency')
    
    plt.show()
    
    #  Plot 2: Line chart
    
    ct_borrowers_values = outstanding_balance_line(strip_borrowers_data,
                                                   pos = 7)
    dl_borrowers_values = outstanding_balance_line(strip_borrowers_data,
                                                   pos = 7)
       
    ct_balance_values = outstanding_balance_line(strip_balance_data,pos = 6)
    ct_balance_values = [i * 1000000 for i in ct_balance_values ]
    dl_balance_values = outstanding_balance_line(strip_balance_data,pos = 7)
    dl_balance_values = [i * 1000000 for i in dl_balance_values ]
    
    ct_average_balance = avg_balance_state(ct_balance_values,
                                           ct_borrowers_values)
    dl_average_balance = avg_balance_state(dl_balance_values,
                                           dl_borrowers_values)
    
    plt.plot(ct_average_balance, label='Connecticut Average Balance', 
             linestyle='-' , marker='o', markersize=6, color='b')
    plt.plot(dl_average_balance, label='Delaware Average Balance',
             linestyle='-', marker='s', markersize=6, color='g')
    
    plt.ylabel('Average Balance')
    plt.title('Average Balance Comparison')
    plt.xlabel('Months')
    plt.legend()
    plt.show()
  
if __name__ == "__main__":
    main()