from csv import DictReader, DictWriter
from os import listdir
from os.path import isfile, join

START_DATE = 1996
END_DATE=2006
KEY = "company"
VALUE = "sec_7"

if __name__ == "__main__":
    current_date = START_DATE
    while True:
        if current_date > END_DATE:
            break
        else:
            path = str(current_date)+".tok"
            onlyfiles = [ f for f in listdir(path) if isfile(join(path,f)) ]
            
            o = DictWriter(open(str(current_date)+"_processed.csv", 'w'), ["company", "sec_7"])
            o.writeheader()
            for file_name in onlyfiles:
                data = ""
                with open (path + "/" +file_name, "r") as myfile:
                    data=myfile.read().replace('\n', '')
                d = {KEY: str(file_name), VALUE: data}
                o.writerow(d)
            current_date += 1
