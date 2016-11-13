import sys
import csv

# config
output_header = ["Outlet Type", "Outlet", "Link", "Date", "AuthorId", "AuthorName", "Followers", "Region", "Title", "Snippet"]

print "Hey! I'm a dumb script and the guy who wrote me is a total noob, so you're going to have to help me out."
print "First, I'm going to open the file you gave me"

file = open(sys.argv[1], 'rt')
# name = raw_input('> title: ')

print "Then, I'm going to print out each row and ask you if it is the header row. I'll stop priting when you do, or until I reach the 10th row"
print "(Again, I'm really dumb and the author's a total noob!)"

counter = 0
reader = csv.reader(file)
for row in reader:
    # Some CSV files have giant freaking whitespace
    if len(row) == 0:
        continue
    if counter < 9:
        print "Is this row the header?"
        print "======"
        print row
        print "======"
        confirm_row = raw_input('(y/n, q to quit): ')
        if confirm_row == 'y':
            print "Thanks!"
            header = row
            break;
        elif confirm_row == 'n':
            print "Okay, continuing"
            counter +=1
        elif confirm_row == 'q':
            print "Okay, quitting"
            sys.exit(0)
        else:
            print "Uh, I don't know what that means so I'll just stop"
            sys.exit("terminating")
    else:
        print "Sorry, it looks like we couldn't find the header in the first 10 rows."
        print "Perhaps the CSV file is corrupt or it needs to be edited."
        sys.exit("could not find header row")

print "Great!"
print "This is the header row of the final CSV file we want to produce"
print "=========="
print output_header
print "=========="
print "I'll need you to help me match the columns of the file you gave me to the columns of the final CSV file we want to produce"
print "For reference, this is the row we chose as our header:"
print "=========="
print header
print "=========="

column_indexes = []
for heading in output_header:
    print "What column matches " + heading + "?"
    confirm_column = raw_input("Column (case sensitive): ")
    column_indexes.append(header.index(confirm_column))

print "The column indexes are"
print column_indexes

with open('final.csv', 'w') as csvfile:
    write_final_csv = csv.DictWriter(csvfile, fieldnames=output_header)
    write_final_csv.writeheader();

    # Now loop through the csv file for real
counter = 0
for row in reader:
    if len(row) == 0:
        continue
    if row == header:
        print "Skipping the header"
        continue
    if counter < 3:
        # does python have array mapping functions
        output_file = {}
        for index, column in enumerate(column_indexes):
            try:
                output_file[output_header[index]] = row[column]
            except IndexError:
                output_file[output_header[index]] = ''
        write_final_csv.writerow(output_file);
        counter += 1
