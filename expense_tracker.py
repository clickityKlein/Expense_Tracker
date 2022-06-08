# -*- coding: utf-8 -*-
"""
This program will loop through csv sheets of bank statements. This will
automatically categorize, or prompt to categorize (consults master file).

Program will prompt if csv is Credit or Debit at start.
Program will prompt for date of file being pulled (saved with date pulled in
                                                   format: mm_dd_yyyy)

There will be a master file that stores the descriptions (C2 - C5 below).

Datafields to Import:
    A: Date
    B: Cost
    E: Description
    
Datafields to Export:
    C1: Date
    C2: Description (given)
    C3: Description (keyword)
    C4: Description (local)
    C5: Category
    C6: Recurring (Yes / No)
    C7: Cost
    C8: Credit vs. Debit
"""

import csv

# Importing masterfile and putting into usable format
def masterfile_import(masterfile_path):       
    masterfile_entries = []
    with open(masterfile_path, newline = '') as csvfile:
        mf_reader = csv.reader(csvfile, delimiter = ',')
        for row in mf_reader:
            masterfile_entries.append(row)
    csvfile.close()
    return masterfile_entries

# Importing bank statement (function 1)
# Files are either card_type: Credit or Debit, with date formatted
# as pull_date: mm_dd_yyyy
# resulting in the possible formats: "Credit_mm_dd_yyyy" or "Debit_mm_dd_yyyy"
def statement_info():
    card_type = input('Credit or Debit statement? ')
    pull_date = input('Pull Date: mm_dd_yyyy? ')
    return card_type, pull_date

# Importing bank statement (function 2)
# Takes the path to the folders where the statements are stored, and uses
# the statement information (type, date), to select the correct statement
def import_statement(statement_folder_path):
    statement_specifics = statement_info()
    statement_path = f'{statement_folder_path}{statement_specifics[0]}_{statement_specifics[1]}.csv'
    print(statement_path)
    statements_entries = []
    with open(statement_path, newline = '') as csvfile:
        s_reader = csv.reader(csvfile, delimiter = ',')
        for row in s_reader:
            statements_entries.append(row)
    csvfile.close()
    return statements_entries, statement_specifics

# Gathering data from bank statement
# function to parse through statement and update masterfile with new statement information
# this function will only be prompted if the masterfile doesn't contain the "Keyword"
# Keywords are user provided, and should be something unique to the transaction name
# Keywords should also be entered in lowercase (Note: change to automatic lowercase later)
def gather_keys(masterfile, statements, credit_vs_debit):
    new_entries = []
    for statement in statements:
        match = False
        keywords = [entry[1] for entry in masterfile]
        entry_description = statement[4].lower()    
        
        for count, word in enumerate(keywords):
            if word in entry_description:
                match = True
                new_entries.append([statement[0], statement[4], word, masterfile[count][2],
                                    masterfile[count][3], masterfile[count][4],
                                    statement[1], credit_vs_debit])
                continue
        
        # categories can be altered here, and are merely recommendations (i.e. a brand new category won't trigger an error warning)
        categories = 'Income\nSavings\nUtilities\nHousing\nFood\nTransportation\nInsurance\nDebt\nLeisure\nEducation\nPersonal\nMisc'
        if match != True:
            print(statement)
            new_key = input('Please provide a Keyword: ')
            new_local = input('Please provide a Local Description: ')
            new_category = input('Please provide a Category: \n' + categories + '\n')
            new_recurring = input('Is this a Recurring charge?: ')
            keywords.append(new_key)
            masterfile.append([statement[4], new_key, new_local, new_category, new_recurring])
            new_entries.append([statement[0], statement[4], new_key, new_local, new_category,
                                new_recurring, statement[1], credit_vs_debit])
    return new_entries

# This function combines the above functions into a single call, and updates appropriate external files
def run_export(masterfile_path, statement_folder_path, export_path):
    # Call individual functions
    masterfile_entries = masterfile_import(masterfile_path)
    statement_entries = import_statement(statement_folder_path)
    new_entries = gather_keys(masterfile_entries, statement_entries[0], statement_entries[1][0])
    
    # Save updated masterfile back
    masterfile = open(masterfile_path, 'w', newline = '\n')
    data = csv.writer(masterfile)
    for entry in masterfile_entries:
        data.writerow(entry)
    masterfile.close()
    
    # Combine data to add to export file
    export_file = f'{export_path}export_complete_{statement_entries[1][0]}_{statement_entries[1][1]}.csv'
    export_complete = open(export_file, 'w', newline = '\n')
    data = csv.writer(export_complete)
    for transaction in new_entries:
        data.writerow(transaction)
    export_complete.close()