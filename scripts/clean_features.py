from csv import DictReader, DictWriter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import SVR
from scipy.sparse import csr_matrix, vstack, hstack
from os import listdir
from os.path import isfile, join
import getpass
import csv
import sys
import itertools
import string

import numpy as np

if __name__ == "__main__":
    current_year = 2001
    END_DATE = 2006
    while True:
        if current_year > END_DATE:
            break
        else:
            with open("./feat_data/" +str(current_year)+"_features_2.csv", "a") as analysisfile:
                analysisfile.write("Identifier,CIK,Ticker,Co_name,IPO_year,Sector,Industry,Historical_Volatilities,Wikipedia_1st_Sent\n")
                csv = list(DictReader(open("./feat_data/" +str(current_year) + "_features_1.csv", 'rU')))
                csv = sorted(csv)
                dirs = listdir( "./org_data/" +str(current_year) + "_train_x/" )
                dirs = sorted(dirs)
                print "DIRS ", len(dirs)
                print "FEATURES", len(csv)
                found_count = 0
                not_found = 0
                for name in dirs:
                    found = 0
                    for x in csv:
                        if name == str(x['Identifier'])+".mda":
                            found_count = found_count + 1
                            found = 1
                            analysisfile.write(str(x['Identifier'])+"," + str(x['CIK']) + "," + str(x['Ticker']) + "," + str(x['Co_name']) + "," + str(x['IPO_year']) + "," + str(x['Sector']) + "," + str(x['Industry']) + "," + str(x['Historical_Volatilities']) + "," + str(x['Wikipedia_1st_Sent']) + "\n")
                            break
                    if found == 0:
                        not_found = not_found + 1
                        array = name.split('.')
                        analysisfile.write(array[0]+", , , , , , , , \n")
                print 'found_count' , found_count
                print 'not_found' , not_found



            current_year = current_year +1
