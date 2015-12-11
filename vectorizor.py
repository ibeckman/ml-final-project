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

class Featurizer:
    def __init__(self, vec_int, feat, norm_val, ngram):
        if vec_int == 1:
            self.vectorizer = CountVectorizer(input='filename', min_df=feat, stop_words='english', norm=norm_val, ngram_range=(1,ngram))
            self.vectorizer2 = CountVectorizer(input='content', max_features=75 ,stop_words='english', norm=norm_val)
        elif vec_int == 2:
            self.vectorizer = TfidfVectorizer(input='filename', min_df=feat, stop_words='english', norm=norm_val, ngram_range=(1,ngram), sublinear_tf=True)
            self.vectorizer2 = TfidfVectorizer(input='content', max_features=75, stop_words='english', norm=norm_val, sublinear_tf=True)
        else:
            self.vectorizer = HashingVectorizer(input='filename', min_df=feat, stop_words='english', norm=norm_val, ngram_range=(1,ngram))
            self.vectorizer2 = HashingVectorizer(input='content',max_features=75, stop_words='english', norm=norm_val)


    def train_feature(self, examples):
        return self.vectorizer.fit_transform(examples)
    
    def test_feature(self, examples):
        return self.vectorizer.transform(examples)
    
    def load_features_data(self, x_data, file_name, feature_names):
        input = list(DictReader(open(file_name, 'rU')))
        features = sorted(input)
        feat_count = 10
        for y in feature_names:
            if y == 'IPO_year':
                feat_count = 35
            elif y == 'Sector':
                feat_count = 15
            elif y == 'Industry':
                feat_count = 75
            elif y == 'Wikipedia_1st_Sent':
                feat_count = 75
            vectorizer3 = TfidfVectorizer(input='content', max_features=feat_count, stop_words='english', norm='l1', sublinear_tf=True)
            feat_train = vectorizer3.fit_transform(x[y] for x in features)
            x_data = hstack([x_data,feat_train])
        return x_data

    def load_historical_data(self, x_data, file_name, col_value):
        features = list(DictReader(open(file_name, 'rU')))
        features = sorted(features)
        hist_feat = []
        total = 0.0
        for x in features:
            total = total + float(x[col_value])
        for x in features:
            row = [float(x[col_value])/total]
            hist_feat.append(row)
        print hist_feat
        csr_hist = csr_matrix(np.array(hist_feat, dtype=float))
        result = hstack([x_data,csr_hist])
        return result

    def load_train_data(self, x_file_name, y_file_name):
        dirs = listdir( x_file_name )
        for i in range(0,len(dirs)):
            dirs[i] = x_file_name+dirs[i]

        dirs = sorted(dirs)

        x_train = self.train_feature(dirs)

        with open(y_file_name, 'rb') as f:
            csv_reader = csv.reader(f)
            your_list = list(csv_reader)
        merged = list(itertools.chain.from_iterable(your_list))

        y_train = [float(i) for i in merged]
 
        return (x_train, y_train)

    def load_test_data(self, x_file_name, y_file_name):
        dirs2 = listdir(x_file_name)
        for i in range(0,len(dirs2)):
            dirs2[i] = x_file_name+dirs2[i]
                    
        dirs2 = sorted(dirs2)
        
        x_test = self.test_feature(dirs2)

        with open(y_file_name, 'rb') as f:
            csv_reader = csv.reader(f)
            your_list = list(csv_reader)
                
        merged2 = list(itertools.chain.from_iterable(your_list))
        y_test = [float(i) for i in merged2]
                                
        return (x_test, y_test)


