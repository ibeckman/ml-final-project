from csv import DictReader, DictWriter
from os import listdir
from os.path import isfile, join

START_DATE = 1996
END_DATE=2006
KEY = "company"
VALUE = "sec_7"
LABEL = "volatility"

if __name__ == "__main__":
    current_date = START_DATE
    while True:
        if current_date > END_DATE:
            break
        else:
            file_name_test = str(current_date)+"_processed.csv"
            file_name_train = str(current_date)+"_training.csv"
            labels_file_name = str(current_date)+".logvol.+12.txt"
            
            labels = {}
            with open(labels_file_name) as infile:
                for line in infile:
                    arr = line.split()
                    labels[arr[1]+".mda"] = arr[0];
        
            o = DictWriter(open(file_name_train, 'w'), [KEY, VALUE, LABEL])
            o.writeheader()

            count = 0
            
            with open(file_name_test, 'r') as infile2:
                for entry in infile2:
                    if count > 0:
                        arr2 = entry.split(',')
                        company_name = str(arr2[0])
                        d = {KEY: company_name, VALUE: arr2[1], LABEL: labels.get(company_name)}
                        o.writerow(d)
                    else:
                        count = 1
            current_date += 1
