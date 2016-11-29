import sys
import os
import json
import csv
from pprint import pprint

# Const - config
CONFIG = [];

# Const - list of files
CSV_FILES = [];

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

def parse_infomart(path):
    # Config for infomart
    infomart_config = '';
    # Header for an infomart file. If this doesn't exist in the csv file, we skip the file
    infomart_header = [];

    print "parsing " + path + " using infomart schema"
    for conf in CONFIG:
        if conf['type'] == 'infomart':
            infomart_config = conf

    print "parsing header row"
    for col in conf['schema']:
        if 'delete' in col and col['delete'] == False:
            infomart_header.append(str(col['title']))

    print infomart_header

    # file = open(path, 'rt')
    #
    # reader = csv.reader(file)
    # for row in reader:
    #     if len(row) == 0:
    #         continue

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
