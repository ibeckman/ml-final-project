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
import matplotlib.pyplot as plt

class Accuracy:
    def __init__(self, y_lin_temp, y_test_temp):
        self.y_lin = y_lin_temp
        self.y_test = y_test_temp
    
    def squareError(self):
        sum_square_err = 0           #sum of (log(v) - log(v_predicted))^2
        numerr = 0              #number of differences greater than 0.5
        
        for i in range(len(self.y_test)):    #computing the sum of
            err = (self.y_test[i] - self.y_lin[i])
            if (err > 0.5 or err < -0.5):
                numerr += 1
            error = self.y_test[i] - self.y_lin[i]
            sum_square_err += math.pow(error, 2)
        return (sum_square_err/len(self.y_test))

    def numberOfErrors(self):
        numerr = 0 #number of differences greater than 0.5
        for i in range(len(self.y_test)):    #computing the sum of
            err = (self.y_test[i] - self.y_lin[i])
            if (err > 0.5 or err < -0.5):
                numerr += 1
        return numerr

    def plotGraph(self):
        plt.plot(self.y_test, label='data')
        plt.hold('on')
        plt.plot(self.y_lin, label='linear model')
        plt.title('Support Vector Regression')
        plt.legend()
        plt.show()

