
from csv import DictReader, DictWriter
from sklearn.svm import SVR
from os import listdir
from os.path import isfile, join
import csv
import getpass
import sys
import math
import argparse

import numpy as np
from sklearn.svm import SVR
from scipy.sparse import csr_matrix

class SVRegression:
    def __init__(self, kernel_value, c_value, iter_value):
        self.kernel = kernel_value
        self.c = c_value
        self.iter = iter_value
        self.svr_lin = None
    
    def fit_predict(self, x_train, y_train, x_test):
        self.svr_lin = SVR(kernel=self.kernel, C=self.c, max_iter=self.iter)
        y_lin = self.svr_lin.fit(x_train, y_train).predict(x_test)
        return y_lin
    
    def computeC(self, x_train):
        print "ARRAY ", type(x_train)
        print x_train
        array = x_train.todense()
        print "ARRAY ", type(array)
        print array
        result = array.sum(axis=1, dtype='float')
        result = pow(result, 2)
        total = result.sum(axis=0, dtype='float')
        rows, columns = x_train.shape
        total = float(total)/float(rows)
        total = pow(total,-1)
        print "C", total
        self.c = total

    def computeAccuracy(self, x, y):
        return self.svr_lin.score(x, y)

if __name__ == "__main__":
    array = np.random.rand(3,2)
    print "array ", array
    array = csr_matrix(array)
    print "type array " , type(array)
    print "array ", array
    array = array.todense()
    print "ARRAY ", type(array)
    result = array.sum(axis=1, dtype='float')
    print "sum row ", result
    result = pow(result, 2)
    print "power" , result
    total = result.sum(axis=0)
    print "sum column" , total
    rows, columns = array.shape
    print "shape", array.shape
    print total
    total = float(total)/float(rows)
    print "divided" , total
    total = pow(total,-1)
    print "INVERTED ", total



