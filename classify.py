from io import BytesIO, StringIO
from zipfile import ZipFile
import urllib.request
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import pickle
import numpy as np

def load_train():
    url = urllib.request.urlopen('http://cs.stanford.edu/people/alecmgo/trainingandtestdata.zip')
    zipfile = ZipFile(BytesIO(url.read()))
    trainfile = zipfile.open('testdata.manual.2009.06.14.csv')
    train = pd.read_csv(trainfile,header=None,names=['polarity', 'id', 'date','query', 'user', 'text'])
    return train

def predict_label(X_train,y_train,X_test):
    model = LogisticRegression()
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    return pred

def map_polarity(pred,X_test):
    positives = []
    negatives = []
    
    for i in range(len(pred)):
        if pred[i]==4:
            positives.append(X_test[i])
        if pred[i]==0:
            negatives.append(X_test[i])
    return positives, negatives

def write_file(data,fileName):
    n = open(fileName, 'w')
    for k in data:
        #print(k)
        n.write(k+"\n")
    n.close()

def main():
    train = load_train()
    Cvectorizer = CountVectorizer(min_df=1, ngram_range=(1,1))
    X_train = Cvectorizer.fit_transform(train['text'])
    
    tweets=pickle.load( open( "DataStore/tweets.p", "rb" ) )
    test = set()
    for t in tweets:
        test.add(t)
    test=list(test)
    X_test =  Cvectorizer.transform(test)
    # Print part of the vocabulary.
    vocab = np.array(Cvectorizer.get_feature_names())
    y_train = np.array(train['polarity'])
    pred = predict_label(X_train,y_train,X_test)
    pos,neg = map_polarity(pred,test)
    write_file(pos,'DataStore/PositiveTweets.txt')
    write_file(neg,'DataStore/NegativeTweets.txt')
    classifyResult={}
    classifyResult['total'] = len(test)
    classifyResult['positive'] = len(pos)
    classifyResult['negative'] = len(neg)
    
    
    print("============Result============")
    print("Number of Positive tweets : %d "%(len(pos)))
    print("Number of Negative tweets : %d "%(len(neg)))
    print("-----------------------------------------------------------")
    print("Positive Tweet")
    print(pos[1])
    classifyResult['posTweet'] = pos[1]
    print("-----------------------------------------------------------")
    print("Negative Tweet")
    print(neg[1])
    classifyResult['negTweet'] = neg[1]
    pickle.dump(classifyResult, open( "DataStore/classifyResult.p", "wb" ))
    print(classifyResult)

if __name__ == '__main__':
    main()
