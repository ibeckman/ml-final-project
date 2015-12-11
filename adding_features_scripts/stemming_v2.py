
import io
import os.path, sys
import numpy
import nltk
from numpy import array
from nltk.stem.snowball import SnowballStemmer

import random
import re

def pre_process():
        st = SnowballStemmer("english")
        to_stem_data = []
        data = numpy.genfromtxt(fname = "00086T103-10-K-20010321.mda", dtype = str, unpack = True, comments = '}')
        print data
        data_stemmed = []
        for i in range(0,len(data)):
        #for sentence in data:
            words_split = []
            words_stem = []
            words_join = []
            sentence = data[i]
            words_split = sentence.split(" ")
            words_stem = [st.stem(j) for j in words_split]
            words_join = ' '.join(words_stem)
            data_stemmed.append(words_join)
        print data_stemmed
        return 5


if __name__ == "__main__":
	pre_process()