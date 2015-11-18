import os
import pickle
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from sklearn.naive_bayes import MultinomialNB

data_path1='../data/a_pos'
pos= os.path.abspath(os.path.join(os.path.dirname(__file__),data_path1))

data_path2='../data/a_neg'
neg= os.path.abspath(os.path.join(os.path.dirname(__file__),data_path2))

test_path1='../data/testpos'
testpos= os.path.abspath(os.path.join(os.path.dirname(__file__),test_path1))

test_path2='../data/testneg'
testneg= os.path.abspath(os.path.join(os.path.dirname(__file__),test_path2))

from sklearn.metrics import accuracy_score

stemmer = SnowballStemmer('english')

labels=[]
text=[]

def parse(f,pol):

    for i in f:
        i = i.strip()
        if len(i) == 0:
            continue
        
            
        text.append(i)

        if(pol == 'pos'):
            labels.append(1)
        else:
            labels.append(0)    

                                
def createPickle(name,dict):
    fileObject = open(name,'wb') 
    pickle.dump(dict,fileObject)   
    fileObject.close()    

    
def loadPickle(name):
    fileObject = open(name,'r')  
    b = pickle.load(fileObject)  
    fileObject.close()
    return b
        
def train():        
    fileObject = open(pos, 'r')  
    text1 = fileObject.readlines()
    parse(text1,'pos')
    
    fileObject = open(neg,'r')  
    text2 = fileObject.readlines()
    parse(text2,'neg')
    
    
    lab= np.array(labels)
    
    vectorizer = TfidfVectorizer()
    features = vectorizer.fit_transform(text)
    
    clf1 = MultinomialNB()
    clf1.fit(features, lab)
    
    createPickle('vect.pkl', vectorizer)
    createPickle('svm.pkl',clf1)
    fileObject.close()
    
    print 'training done'

def test():
    
    clf = loadPickle('svm.pkl')
    vec = loadPickle('vect.pkl')
    
    fileObject = open(testpos, 'r')  
    text1 = fileObject.readlines()
    parse(text1,'pos')
    
    fileObject = open(testneg,'r')  
    text2 = fileObject.readlines()
    parse(text2,'neg')
    
    testset = vec.transform(text)

    out=clf.predict(testset)
    exp_out=np.array(labels)
    
    print accuracy_score(out, exp_out)
#train()       
#test()        

def main():    
    
    global labels, text

    fileObject = open(pos, 'r')  
    text1 = fileObject.readlines()
    parse(text1,'pos')
    
    fileObject = open(neg,'r')  
    text2 = fileObject.readlines()
    parse(text2,'neg')
    
    
    lab= np.array(labels)
    
    
    vec = TfidfVectorizer(stop_words='english',max_df=0.5)
    features = vec.fit_transform(text)
    
    clf = MultinomialNB(fit_prior=False)
    clf.fit(features, lab)
    
    print 'training done'

    text=[]
    labels=[]
    
    fileObject = open(testpos, 'r')  
    text1 = fileObject.readlines()
    parse(text1,'pos')
    
    fileObject = open(testneg,'r')  
    text2 = fileObject.readlines()
    parse(text2,'neg')
    
    testset = vec.transform(text)

    out=clf.predict(testset)
    exp_out=np.array(labels)
    
    print out
    print exp_out
    
    print accuracy_score(out, exp_out)
    print clf.coef_
 
main()    
'''
l=[]
[l.append((v,k)) for (k,v) in idf.items()]
l.sort(reverse=True)
for i in range(50):
    print l[i]
'''