# Assignment 1: Text Processing with Python
# Tera Parish
# txp200011

import sys
import pathlib
import re
import pickle
import nltk
from nltk import word_tokenize


# person class
class Person:
    def __init__(self, list):
        self.last = list[0]
        self.first = list[1]
        self.mi = list[2]
        self.id = list[3]
        self.phone = list[4]

    def display(self):
        print('Employee id:', self.id)
        print('\t', self.first, self.mi, self.last)
        print('\t', self.phone, '\n')


def process_data(rows):
    # build an employee dict
    # key = id, value = person obj
    emps = {}

    # iterate through the list
    for r in rows:
        # split on comma
        # [0-4] = Last, First, Middle Initial, ID, Office phone
        fields = r.split(',')

        # format name
        fields[0] = fields[0].capitalize()
        fields[1] = fields[1].capitalize()
        if fields[2].islower():
            fields[2] = fields[2].upper()
        elif not fields[2]:
            fields[2] = 'X'

        # validate id: 2 letters followed by 4 digits
        regex_id = '^[A-Z]{2}\d{4}'
        while not re.match(regex_id, fields[3]):
            print('\nID invalid:', fields[3])
            print('ID is two letters followed by 4 digits')
            fields[3] = input('Enter a valid ID: ')

        # validate phone number: in form 123-456-7890
        regex_phone = '^\d{3}-\d{3}-\d{4}'
        while not re.match(regex_phone, fields[4]):
            print('\nPhone', fields[4], 'is invalid')
            print('Enter phone number in form 123-456-7890')
            fields[4] = input('Enter phone number: ')

        # add to dict
        emps[fields[3]] = Person(fields)

    return emps


# standard way to start a program
if __name__ == '__main__':
    # check if a system argument is passed in
    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')
        quit()

    rel_path= sys.argv[1]
    with open(pathlib.Path.cwd().joinpath(rel_path), 'r') as f:
        # read in the entire file, split on new line char
        # text_in = list[str]
        text_in = f.read().splitlines()

    # employees = dict
    # skip the heading line
    employees = process_data(text_in[1:])

    # pickle the employees
    # wr = write binary
    pickle.dump(employees, open('employees.pickle', 'wb'))

    # read the pickle back in
    # rb = read binary
    employees_in= pickle.load(open('employees.pickle', 'rb'))

    # output employees
    print('\n\nEmployee list:\n')
    for key, value in employees_in.items():
        value.display()