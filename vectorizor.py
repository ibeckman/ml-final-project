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

START_DATE = 2001
END_DATE=2001
KEY = "company"
VALUE = "sec_7"

class Featurizer:
    def __init__(self, vec_int):
        if vec_int == 1:
            self.vectorizer = CountVectorizer(stop_words='english')
        elif vec_int == 2:
            self.vectorizer = TfidfVectorizer(stop_words='english')
        else:
            self.vectorizer = HashingVectorizer(stop_words='english')
    
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
    
    current_year = END_DATE

    feat2 = Featurizer(0)
    
    while True:
        if current_year > END_DATE:
            break
        else:
            #with open("./data/" + str(current_year)+"_agg_data.csv", 'r') as outfile:
            #x_train = feat2.train_feature(outfile)
            labels = []
            for row in DictReader(open("./data/" +str(current_year)+"_agg_label_data.csv", 'r')):
                labels.append(row[0])
            print labels

        current_year += 1

    #feat1 = Featurizer1()

    #feat3 = Featurizer3()
    
    """
    train1 = list(DictReader(open("1996_processed.csv", 'r')))
    train2 = list(DictReader(open("1997_processed.csv", 'r')))
    train3 = list(DictReader(open("1998_processed.csv", 'r')))
    train4 = list(DictReader(open("1999_processed.csv", 'r')))
    train5 = list(DictReader(open("2000_processed.csv", 'r')))
    """

    """
    x_train = feat2.train_feature(x[VALUE] for x in train5)
    x_train = feat2.train_feature(x[VALUE] for x in train4)
    x_train = feat2.train_feature(x[VALUE] for x in train3)
    x_train = feat2.train_feature(x[VALUE] for x in train2)
    x_train = feat2.train_feature(x[VALUE] for x in train1)
    """
    #x3_train1 = feat3.train_feature(x[VALUE] for x in train1)
    
    #print x1_train1.shape
#print x_train.shape
#print x3_train1.shape


"""
    x1_train1 = feat1.train_feature(x[VALUE] for x in train1)
    x2_train1 = feat2.train_feature(x[VALUE] for x in train1)
    x3_train1 = feat3.train_feature(x[VALUE] for x in train1)
    
    print x1_train1.shape
    print x2_train1.shape
    print x3_train1.shape
    """

#x_train = feat.train_feature(x[VALUE] for x in train1)
#print x_train.shape
#print x_train

#vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5, stop_words='english')
#vectorizer = HashingVectorizer(stop_words='english', non_negative=True)
#x_train = vectorizer.fit_transform(x[VALUE] for x in train)
#featurenames = np.asarray(vectorizer.get_feature_names())
#print featurenames
#print x_train.shape
#print x_train

#tf_transformer = TfidfTransformer(use_idf=False).fit(x_train)
#x_train_tf = tf_transformer.transform(x_train)
#print x_train_tf.shape
#print x_train_tf

"""
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
