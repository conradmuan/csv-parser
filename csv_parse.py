import sys
import os
import json
import csv
import hashlib
from pprint import pprint

# Const - config
CONFIG = [];

# Const - list of files
CSV_FILES = [];

# Header row for the final file
OUTPUT_HEADER = ['Outlet Type', 'Outlet', 'Link', 'Date', 'AuthorId', 'AuthorName', 'Followers', 'Region', 'Title', 'Snippet']

# Open the config and store as a constant
def get_config():
    with open('config.json') as config_file:
        return json.load(config_file)

CONFIG = get_config();

# Open a folder and return its contents as a list if each item is a csv
def get_csv_files(folder_path=None):
    if folder_path is None:
        folder_path = 'raw_data'
    csv_count = 0;
    for item in os.listdir(folder_path):
        root, ext = os.path.splitext(item)
        if ext == '.csv':
            csv_count += 1
            CSV_FILES.append(item);
    # Exit if no csv files were found
    if csv_count == 0:
        sys.exit("Directory " + argv[1] + " does not have any csv files :(")

# Erorr catching, exit when no args
# try:
#     get_csv_files(sys.argv[1]);
# except:
#     sys.exit("Please provide a directory to read");

# Loop through each list and detect if the item is a sysomos or an infomart

def parse_file(filepath, type):
    # The value of a CONFIG index for type
    config = ''
    # fieldnames we'll be saving
    fields = []
    # the index of the field we want to save
    field_index_map = {}
    # the file to parse
    file = open(filepath, 'rt')

    for conf in CONFIG:
        if conf['type'] == type:
            config = conf

    for col in config['schema']:
        fields.append(str(col['title']))

    print fields

    reader = csv.reader(file)
    # Get the index of the fieldname in the file's header
    # We will a ttempt to get the header in 10 tries
    for index, row in enumerate(reader):
        if index < 10:
            for fieldname in fields:
                if fieldname in row:
                    field_index_map[fieldname] = row.index(fieldname)
                else:
                    # If the first fieldname wasn't in the row, safe to skip the row entirely
                    break
    print field_index_map

# Custom logic for infomart
def parse_infomart(filepath):
    expected_header_row = ['Publication','Date','Region','Media','Tone','Ad Value','Circulation','Link','Byline','Page','Length','Title','Lead']
    # Temporary output file name
    temp_output_file_name = hashlib.md5(filepath).hexdigest();
    # Temporary output file
    temp_output_file = ''
    # Temporary output file row
    temp_output_file_row = {}

    with open(temp_output_file_name+'.csv', 'w') as csv_file:
        temp_output_file = csv.DictWriter(csv_file, fieldnames=OUTPUT_HEADER)
        temp_output_file.writeheader()

        with open(filepath, 'rt') as file:
            csv_file = csv.reader(file)
            for index, row in enumerate(csv_file):
                
                if len(row) == 0:
                    continue
                if row == expected_header_row:
                    # This is the header row
                    continue
                # Start building out the rows
                # I don't feel good about this approach :(
                for idx, col_header in enumerate(OUTPUT_HEADER):
                    if col_header == 'Outlet Type':
                        temp_output_file_row[col_header] = 'NEWS'
                    if col_header == 'Outlet':
                        temp_output_file_row[col_header] = row[expected_header_row.index('Publication')]
                    if col_header == 'Link':
                        temp_output_file_row[col_header] = row[expected_header_row.index('Link')]
                    if col_header == 'Date':
                        temp_output_file_row[col_header] = row[expected_header_row.index('Date')]
                    if col_header == 'AuthorId':
                        temp_output_file_row[col_header] = row[expected_header_row.index('Byline')]
                    if col_header == 'AuthorName':
                        temp_output_file_row[col_header] = row[expected_header_row.index('Byline')]
                    if col_header == 'Followers':
                        temp_output_file_row[col_header] = row[expected_header_row.index('Circulation')]
                    # todo, we need to abbreviate
                    if col_header == 'Region':
                        temp_output_file_row[col_header] = row[expected_header_row.index('Region')]
                    if col_header == 'Title':
                        temp_output_file_row[col_header] = row[expected_header_row.index('Title')]
                    if col_header == 'Snippet':
                        temp_output_file_row[col_header] = row[expected_header_row.index('Lead')]

                temp_output_file.writerow(temp_output_file_row)
    return

def parse_sysomos(file):
    print "parsing sysomos for " + file

def determine_user_prompt(prompt, file):
    if prompt == "infomart" or prompt == "i":
        parse_infomart(file)
    elif prompt == "sysomos" or prompt == "s":
        parse_sysomos(file)
    elif prompt == "skip":
        print "skipping!"
    elif prompt == "quit" or prompt == "q":
        sys.exit("Quitting!")
    else:
        # Todo add some logging here
        print "I don't know what that means, skipping!"

def iterate_over_csv_files():
    for item in CSV_FILES:
        if "sysomos" in item.lower():
            parse_sysomos(item)
        elif "infomart" in item.lower():
            parse_infomart(item)
        else:
            print "Cannot determine type of csv file (sysomos/infomart). Please tell me."
            custom = raw_input("infomart/sysomos/skip/quit: ")
            determine_user_prompt(custom, item)
# Run it
# iterate_over_csv_files();
parse_infomart('raw_data/Database Infomart 2.csv')
