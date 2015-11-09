from csv import DictReader, DictWriter
from os import listdir
from os.path import isfile, join

START_DATE = 2001
END_DATE=2006
KEY = "company"
VALUE = "sec_7"

if __name__ == "__main__":
    current_year = START_DATE
    while True:
        if current_year > END_DATE:
            break
        else:
            count = 5
            with open( str(current_year) + "_agg_data.csv", 'w') as outfile:
                while count > 0:
                    file_name = str(current_year-count) + "_processed.csv"
                    with open(file_name) as infile:
                        for line in infile:
                            outfile.write(line)
                    count -= 1
            count = 5
            with open(str(current_year)+ "_agg_label_data.txt", 'w') as outfile:
                while count > 0:
                    file_name = str(current_year-count) + ".logvol.+12.txt"
                    with open(file_name) as infile:
                        for line in infile:
                            outfile.write(line)
                    count -= 1
            current_year += 1
