import sys
import os
import json
import csv

# Const - list of files
CSV_FILES = []

# Header row for the final file
OUTPUT_HEADER = ['Outlet Type', 'Outlet', 'Link', 'Date', 'AuthorId', 'AuthorName', 'Followers', 'Region', 'Title', 'Snippet']

# Output File handler
OUTPUT_FILE_HANDLER = open('final.csv', 'w')

# Output CSV file
OUTPUT_FILE = csv.DictWriter(OUTPUT_FILE_HANDLER, fieldnames=OUTPUT_HEADER)
OUTPUT_FILE.writeheader()

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
    # Header row of an infomart csv file
    expected_header_row = ['Publication','Title','Lead','Byline','Page','Length','Date','Region','Media','Tone','Ad Value','Circulation','Link','Note']

    output_file_row = {}

    province_abbr_map = {'ontario': 'on', 'quebec': 'qc', 'british columbia': 'bc', 'alberta': 'ab', 'manitoba': 'mb', 'saskatchewan': 'sk', 'nova scotia': 'ns', 'new brunswick': 'nb', 'newfoundland and labrador': 'nl', 'newfoundland': 'nl', 'prince edward island': 'pe', 'pei': 'pe'}

    with open(filepath, 'rt') as file:
        csv_file = csv.reader(file)
        for index, row in enumerate(csv_file):
            # Todo: Validate that we have a header row somewhere in the first 10 rows
            # Temp, remove this shit
            if index < 3:
                if len(row) == 0:
                    continue
                if row == expected_header_row:
                    # This is the header row
                    continue
                # Start building out the rows
                # I don't feel good about this approach :(
                for col_header in OUTPUT_HEADER:
                    if col_header == 'Outlet Type':
                        output_file_row[col_header] = 'NEWS'
                    if col_header == 'Outlet':
                        output_file_row[col_header] = row[expected_header_row.index('Publication')]
                    if col_header == 'Link':
                        output_file_row[col_header] = row[expected_header_row.index('Link')]
                    if col_header == 'Date':
                        output_file_row[col_header] = row[expected_header_row.index('Date')]
                    if col_header == 'AuthorId':
                        output_file_row[col_header] = row[expected_header_row.index('Byline')]
                    if col_header == 'AuthorName':
                        output_file_row[col_header] = row[expected_header_row.index('Byline')]
                    if col_header == 'Followers':
                        output_file_row[col_header] = row[expected_header_row.index('Circulation')]
                    if col_header == 'Region':
                        if row[expected_header_row.index('Region')].lower() in province_abbr_map:
                            output_file_row[col_header] = province_abbr_map[row[expected_header_row.index('Region')].lower()]
                        else:
                            output_file_row[col_header] = row[expected_header_row.index('Region')]
                    if col_header == 'Title':
                        output_file_row[col_header] = row[expected_header_row.index('Title')]
                    if col_header == 'Snippet':
                        output_file_row[col_header] = row[expected_header_row.index('Lead')]

                OUTPUT_FILE.writerow(output_file_row)
    # temp
    OUTPUT_FILE_HANDLER.close()
    return

def parse_sysomos(filepath):
    # Expected header row for a sysomos file
    expected_header_row = ["No.","Source","Host","Link","Date(ET)","Time(ET)","time(Eastern Standard Time)","Category","AuthorId","AuthorName","AuthorUrl","Auth","Followers","Following","Age","Gender","Language","Country","Province","City","Location","Sentiment","Title","Snippet","Description","Tags","Contents","View","Comments","Rating","Favourites","Duration","Bio","UniqueId"]

    output_file_row = {}

    with open(filepath, 'rt') as file:
        csv_file = csv.reader(file)
        for index, row in enumerate(csv_file):
            # Todo: validation
            # temp remove this
            if index < 10:
                if len(row) == 0:
                    continue
                if row == expected_header_row:
                    continue
                # skip a bad row unique to this type of csv file
                if row[0] == 'Search Results' and row[len(row)-1] == '':
                    continue
                # build out the output_file_row
                for col_header in OUTPUT_HEADER:
                    if col_header == 'Outlet Type':
                        output_file_row[col_header] = row[expected_header_row.index('Source')]
                    if col_header == 'Outlet':
                        output_file_row[col_header] = row[expected_header_row.index('Host')]
                    if col_header == 'Link':
                        output_file_row[col_header] = row[expected_header_row.index('Link')]
                    if col_header == 'Date':
                        output_file_row[col_header] = row[expected_header_row.index('Date(ET)')]
                    if col_header == 'AuthorId':
                        output_file_row[col_header] = row[expected_header_row.index('AuthorId')]
                    if col_header == 'AuthorName':
                        output_file_row[col_header] = row[expected_header_row.index('AuthorName')]
                    if col_header == 'Followers':
                        output_file_row[col_header] = row[expected_header_row.index('Followers')]
                    if col_header == 'Region':
                        if row[expected_header_row.index('Province')] == '':
                            output_file_row[col_header] = 'NA'
                        else:
                            output_file_row[col_header] = row[expected_header_row.index('Province')]
                    if col_header == 'Title':
                        output_file_row[col_header] = row[expected_header_row.index('Title')]
                    if col_header == 'Snippet':
                        output_file_row[col_header] = row[expected_header_row.index('Snippet')]
                OUTPUT_FILE.writerow(output_file_row)
    # temp
    OUTPUT_FILE_HANDLER.close()
    return

def determine_user_prompt(prompt, file):
    if prompt == "infomart" or prompt == "i":
        parse_infomart(file)
    elif prompt == "sysomos" or prompt == "s":
        parse_sysomos(file)
    elif prompt == "skip":
        with open('skipped.txt', 'a') as logfile:
            logfile.write(file)
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

try:
    get_csv_files(sys.argv[1])
except:
    get_csv_files()

# Run it
# iterate_over_csv_files()

parse_infomart('raw_data/Rheumatology - infomart.csv')
