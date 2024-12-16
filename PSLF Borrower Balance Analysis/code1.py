'''
    DS2500
    Fall 2023
    Code from class -- student loan data 
    
    For class, we have one csv file representing one month of data.
    The data is cumulative, so for November 2022 we have...
        - state
        - number of borrowers (total borrowers up to and including Nov 2022
                               who have had their PSLF applications discharged)
        - outstanding balance (total outstanding balance as of Nov 2022,
                               that the borrowers still owe after PSLF)
                               
    
    Note that the dataset has dollar amounts in millions (e.g., they have
                                                          100 == 100 mil), 
    but on the homework we'll ask for "actual" values (100,000,000)'
    
    On the homework, you'll have several files instead of just one!
    
    Code quality notes...
        - Functions should be generic and standalone. If you have a list
            as a parameter, you don't need to also create the list
            inside the function'
        - Print is for humans, return is for computers :)
        - Constants can be used in main but not other funcs
'''

import csv

FILENAME = "pslf_borrowers.csv"

def read_csv(filename, skip_rows = 1, keep_cols = 3):
    ''' read the given CSV into a 2d list of strings and return it.
        Skips the first skip_rows as headers, and keeps only the first
        keep_cols of each rows.
    '''
    data = []
    with open(filename, "r") as infile:
        csvfile = csv.reader(infile)
        for i in range(skip_rows):
            next(csvfile)
        for row in csvfile:
            data.append(row[:keep_cols])
    return data


def sum_column(lst, col = 0):
    ''' Given a 2d list and a column number,
        compute and return the sum of all values in the given column.
        Values in the given column must be numeric.
    '''
    total = 0
    for row in lst:
        total += row[col]
    return total

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
        value = item[1:]
        dct[key] = value
    return dct

def clean_data(lst):
    ''' given a 2d list, convert everything but the first
        element of every row to float
        return a new version of the list, with floats instead of strings
    '''
    cleaned = []
    for row in lst:
        converted = [str_to_float(row[i]) for i in range(1, len(row))]
        cleaned.append(row[:1] + converted)
    return cleaned

    

def main():
    # gather data - read from the csv file into a 2d list
    data = read_csv(FILENAME, skip_rows = 3) 

    # clean up the data - convert strings to floats
    # and create a dictionary so we can look up indv states
    cleaned = clean_data(data)
    data_dct = twod_to_dct(cleaned)
    
    print(data_dct[0][0])
    
    # computation - total borrowers and dictionary
    total_borrowers = sum_column(cleaned, 1)
    total_balance = sum_column(cleaned, 2)


    # communication - report results
    #print(f"Total borrowers who had their loans forgiven: {total_borrowers}")
    #state = input("What state do you want to know about?\n")
    #print(f"Here's your info': {data_dct[state]}")
    
    
if __name__ == "__main__":
    main()
    

    
    
    
    
    
    
    
    
    






