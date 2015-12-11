
from os import listdir
from os.path import isfile, join
import csv
import getpass
import sys
import argparse
from analysis import *
from vectorizor import *
from regression import *
import numpy as np

START_DATE = 2001
END_DATE=2006

if __name__ == "__main__":
    csv.field_size_limit(sys.maxsize)
    
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--vec_int", help="Maximum Number of SVR Iterations",type=list, default=[2], required=False)
    argparser.add_argument("--iter", help="Maximum Number of SVR Iterations",type=list, default=[1250], required=False)
    argparser.add_argument("--feat", help="Maximum Number of Features", type=list, default=[0.0], required=False)
    argparser.add_argument("--norm", help="Normalization Type", type=list, default=['l1'], required=False)
    argparser.add_argument("--ngram", help="N-grams from 1-number provided", type=list, default=[1], required=False)
    argparser.add_argument("--features", help="features to be included in the ", type=list, default=['IPO_year','Sector','Industry','Wikipedia_1st_Sent'], required=False)
    argparser.add_argument("--kernel", help="Kernel option", type=list, default=['linear'], required=False)
    argparser.add_argument("--limit", help="data limit", type=int, default=0, required=False)
    argparser.add_argument("--boost", help="to boost or not to boost", type=int, default=0, required=False)
    argparser.add_argument("--stem", help="to boost or not to boost", type=int, default=0, required=False)
    argparser.add_argument("--c", help="C value to use", type=list, default=[100], required=False)
    
    argparser.add_argument("--debug", help="print debug statements", type=int, default=1, required=False)
    argparser.add_argument("--plot", help="print debug statements", type=int, default=0, required=False)
    
    args = argparser.parse_args()
    
    
    current_year = START_DATE
    
    
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
                                if args.debug == 1:
                                    print "STARTING: creating vectorizor [ " + str(vec_int)+ "]"
                                    print "max features [ " + str(feat) +"]"
                                    print "normalization [ " + str(norm) +"]"
                                    print "ngrams [ 1 to " + str(ngram)+ "]"
                                feat2 = Featurizer(vec_int, feat, norm, ngram)
                                
                                base_dir = "org_data"
                                if args.stem == 1:
                                    base_dir = "stem_data"
                                
                                if args.debug == 1:
                                    print "STARTING: loading training values for training set year [ " + str(current_year) + "]"
                                x_train, y_train = feat2.load_train_data("./"+base_dir+"/"+str(current_year)+"_train_x/", "./org_data/" +str(current_year)+"_train_y.csv")
                                if args.debug == 1:
                                    print "FINISHED: loading training values x_size[ "+str(np.shape(x_train))+" ] y_size [ "+str(np.shape(y_train))+" ] for taining set year [ " + str(current_year) + "]"
                                
                                if args.debug == 1:
                                    print "STARTING: loading testing values for testing year [ " + str(current_year) + "]"
                                x_test, y_test = feat2.load_test_data("./"+base_dir+"/"+str(current_year)+"_test_x/","./org_data/" +str(current_year)+"_test_y.csv")
                                if args.debug == 1:
                                    print "FINISHED: loading testing values x_size[ "+str(np.shape(x_test))+" ] y_size [ "+str(np.shape(y_test))+" ] for testing set year [ " + str(current_year) + "]"
                                
                                if 'Historical_Volatilities' in args.features:
                                    args.features.remove('Historical_Volatilities')
                                    if args.debug == 1:
                                        print "STARTING: loading historical data year [ " + str(current_year) + "]"
                                    x_train = feat2.load_historical_data(x_train, "./feat_data/"+str(current_year)+"_features_2.csv", 'Historical_Volatilities')
                                    x_test = feat2.load_historical_data(x_test, "./feat_data/"+str(current_year)+"_features_test.csv", 'Historical_Volatilities')
                                    if args.debug == 1:
                                        print "FINISHED: loading historical data year [ " + str(current_year) + "]"
                                if args.features:
                                    if args.debug == 1:
                                        print "STARTING: loading extra features for year [ " + str(current_year) + "]"
                                    x_train = feat2.load_features_data(x_train, "./feat_data/"+str(current_year)+"_features_2.csv", args.features)
                                    x_test = feat2.load_features_data(x_test, "./feat_data/"+str(current_year)+"_features_test.csv", args.features)
                                    if args.debug == 1:
                                        print "FINISHED: loading extra features for year [ " + str(current_year) + "]"
                    
                                
                                
                                for iter in args.iter:
                                    for kernel_value in args.kernel:
                                        for c in args.c:
                                            if args.debug == 1:
                                                print "STARTING: SVR with testing year [ " + str(current_year) + "]"
                                                print "Kernel [ " + str(kernel_value) +"]"
                                                print "Iterations [ " + str(iter) +"]"
                                            svreg = SVRegression(kernel_value, c, iter)
                                            #svreg.computeC(x_train)

                                            if args.debug == 1:
                                                print "C Value [ " + str(svreg.c) +"]"
                                                print "STARTING: SVR fit predictions [ " + str(current_year) + "]"
                                            y_lin = svreg.fit_predict(x_train, y_train, x_test)
                                            if args.debug == 1:
                                                print "FINISHED: SVR fit predictions [ " + str(current_year) + "]"
                                                    
                                            acc = Accuracy(y_lin, y_test)
                                            numerr = acc.numberOfErrors()
                                            print "Number of Errors [ " + str(numerr) +"]"
                                            mean_square_err = acc.squareError()
                                            print "Mean Square Value [ " + str(mean_square_err) +"]"

                                            analysisfile.write(str(vec_int)+"," + str(feat) + "," + str(norm) + "," + str(ngram) + "," + str(c) + "," + str(kernel_value) + "," + str(iter) + "," + str(mean_square_err) + "," + str(numerr) + "\n")
                                            
                                            if args.plot == 1:
                                                acc.plotGraph()

        
                                        

        current_year += 1
