from csv import DictReader, DictWriter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import SVR
from os import listdir
from os.path import isfile, join
import csv
import getpass
import sys
import itertools
import math
import argparse

import numpy as np
from sklearn.svm import SVR
import matplotlib.pyplot as plt

START_DATE = 2001
END_DATE=2001
KEY = "company"
VALUE = "sec_7"

class Featurizer:
    def __init__(self, vec_int, feat, norm_val, ngram):
        if vec_int == 1:
            self.vectorizer = CountVectorizer(max_features=feat, stop_words='english', norm=norm_val, ngram_range=(1,ngram))
        elif vec_int == 2:
            self.vectorizer = TfidfVectorizer(max_features=feat, stop_words='english', norm=norm_val, ngram_range=(1,ngram))
        else:
            self.vectorizer = HashingVectorizer(max_features=feat, stop_words='english', norm=norm_val, ngram_range=(1,ngram))
    
    def train_feature(self, examples):
        return self.vectorizer.fit_transform(examples)
    
    def test_feature(self, examples):
        return self.vectorizer.transform(examples)
    
    def show_top10(self, classifier, categories):
        feature_names = np.asarray(self.vectorizer.get_feature_names())
        if len(categories) == 2:
            top10 = np.argsort(classifier.coef_[0])[-10:]
            bottom10 = np.argsort(classifier.coef_[0])[:10]
            print("Pos: %s" % " ".join(feature_names[top10]))
            print("Neg: %s" % " ".join(feature_names[bottom10]))

if __name__ == "__main__":
    csv.field_size_limit(sys.maxsize)
    
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--vec_int", help="Maximum Number of SVR Iterations",type=list, default=[2], required=False)
    argparser.add_argument("--iter", help="Maximum Number of SVR Iterations",type=list, default=[1000], required=False)
    argparser.add_argument("--feat", help="Maximum Number of Features", type=list, default=[50000], required=False)
    argparser.add_argument("--norm", help="Maximum Number of Features", type=list, default=['l1'], required=False)
    argparser.add_argument("--ngram", help="Maximum Number of Features", type=list, default=[1], required=False)
    argparser.add_argument("--kernel", help="Maximum Number of Features", type=list, default=['linear'], required=False)
    argparser.add_argument("--c", help="C value to use", type=list, default=[1], required=False)

    argparser.add_argument("--debug", help="print debug statements", type=int, default=1, required=False)
    argparser.add_argument("--plot", help="print debug statements", type=int, default=0, required=False)
                
    args = argparser.parse_args()
    
    
    current_year = END_DATE

    
    while True:
        if current_year > END_DATE:
            break
        else:
            with open(str(current_year)+"_analysis.csv", "a") as analysisfile:
                analysisfile.write("Vectorizor,Max_Features,Normalization,Ngrams,C,Kernel,Iterations,SqrErr,NumErr\n")
                for vec_int in args.vec_int:
                    for feat in args.feat:
                        for norm in args.norm:
                            for ngram in args.ngram:
                                
                                ###############################################################################
                                # creating vectorizor
                                if args.debug == 1:
                                    print "0.STARTING: creating vectorizor [ " + str(vec_int)+ "]"
                                    print "max features [ " + str(feat) +"]"
                                    print "normalization [ " + str(norm) +"]"
                                    print "ngrams [ 1 to " + str(ngram)+ "]"
                                feat2 = Featurizer(vec_int, feat, norm, ngram)
                                if args.debug == 1:
                                    print "0.FINISHED: creating vectorizor"
                                
                                ###############################################################################
                                # load X values for train set and vectorize them
                                if args.debug == 1:
                                    print "1.STARTING: loading X values for taining set year [ " + str(current_year) + "]"

                                with open("./data/" + str(current_year)+"_agg_data.csv", 'r') as outfile:
                                    next(outfile)
                                    x_train = feat2.train_feature(outfile)

                                if args.debug == 1:
                                    print "X Training Shape: ", x_train.shape
                                    print "1.FINISHED: loading X values for taining set year [ " + str(current_year) + "]"

                                ###############################################################################
                                # load Y values for train set into a list
                                if args.debug == 1:
                                    print "2.STARTING: loading Y values for taining set year [ " + str(current_year) + "]"

                                with open("./data/" +str(current_year)+"_train_y.csv", 'rb') as f:
                                    csv_reader = csv.reader(f)
                                    your_list = list(csv_reader)

                                merged = list(itertools.chain.from_iterable(your_list))

                                y_train = [float(i) for i in merged]

                                if args.debug == 1:
                                    print "Y Training Length: ", len(y_train)
                                    print "2.FINISHED: loading Y values for taining set year [ " + str(current_year) + "]"
                                    
                                ###############################################################################
                                # load X values for test set, vectorize them
                                if args.debug == 1:
                                    print "3.STARTING: loading X values for test set vectorizing year [ " + str(current_year) + "]"

                                with open("./data/" +str(current_year)+"_processed.csv", 'r') as outfile:
                                    next(outfile)
                                    x_test = feat2.train_feature(outfile)
                                        
                                    squared_X = x_test.copy()
                                    # now square the data in squared_X
                                    squared_X.data **= 2
                                                    
                                    # and sum each row:
                                    squared_sum = squared_X.sum(1)
                                        # and delete the squared_X:
                                if args.debug == 1:
                                    print "Final Squared Sum:", squared_sum
                                    print "final average squared sum", np.average(squared_sum)
                                    print "3.FINISHED: loading X values for taining set vectorizing year [ " + str(current_year) + "]"
                                        
                                ###############################################################################
                                # load true Y values for test set
                                if args.debug == 1:
                                    print "4.STARTING: loading true Y values for test set year [ " + str(current_year) + "]"

                                with open("./data/" +str(current_year)+"_test_y.csv", 'rb') as f:
                                    csv_reader = csv.reader(f)
                                    your_list = list(csv_reader)
                                                    
                                merged2 = list(itertools.chain.from_iterable(your_list))
                                y_test = [float(i) for i in merged2]

                                if args.debug == 1:
                                    print "4.FINISHED: loading true Y values for test set year [ " + str(current_year) + "]"
                            
                                ###############################################################################
                                # Train model & predict Y linear

                                for iter in args.iter:
                                    for kernel_value in args.kernel:
                                        for c in args.c:
                                            if args.debug == 1:
                                                print "5.STARTING: SVR for year [ " + str(current_year) + "] with iteration [ "+str(iter)+" ] and C value [ " + str(c) +"] and kernel [ "+ str(kernel_value)+" ]"
                                        
                                            svr_lin = SVR(kernel=kernel_value, C=c, max_iter=iter)
                                            y_lin = svr_lin.fit(x_train, y_train).predict(x_test)
                                    
                                            if args.debug == 1:
                                                print "5.FINISHED: SVR for year [ " + str(current_year) + "] with iteration [ "+str(iter)+" ] and C value [ " + str(c) +"] and kernel [ "+ str(kernel_value)+" ]"
                                        
                                            ###############################################################################
                                            # compute accuracy
                                        
                                            sum_square_err = 0           #sum of (log(v) - log(v_predicted))^2
                                            numerr = 0              #number of differences greater than 0.5
                                            
                                            if args.debug == 1 and (len(y_test) == len(y_lin)):    #just checking if number of predictions equals number of test values (not needed)
                                                print "Test Set Len match"
                                                        
                                            for i in range(len(y_test)):    #computing the sum of
                                                err = (y_test[i] - y_lin[i])
                                                if (err > 0.5 or err < -0.5):
                                                    numerr += 1
                                                error = y_test[i] - y_lin[i]
                                                sum_square_err += math.pow(error, 2)
                                            mean_square_err = (sum_square_err/len(y_test))
                                            print "Mean square error ["+str(iter)+"]["+str(c)+"]", mean_square_err
                                            print "Number of errors["+str(iter)+"]["+str(c)+"]", numerr

                                            ###############################################################################
                                            # Write to File
                                            analysisfile.write(str(vec_int)+"," + str(feat) + "," + str(norm) + "," + str(ngram) + "," + str(c) + "," + str(kernel_value) + "," + str(iter) + "," + str(mean_square_err) + "," + str(numerr) + "\n")

                                            ###############################################################################
                                            # look at the results
                                            if args.plot == 1:
                                                plt.plot(y_test, label='data')
                                                plt.hold('on')
                                                plt.plot(y_lin, label='linear model')
                                                plt.title('Support Vector Regression')
                                                plt.legend()
                                                plt.show()


        current_year += 1
