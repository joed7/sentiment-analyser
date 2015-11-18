''' Python Script to calculate count for Naive Bayes
'''
import os
import pickle
from nltk import word_tokenize
from _collections import defaultdict
from nltk.corpus import stopwords
from nltk.stem.porter import *
import math

data_path1='../data/a_pos'
pos= os.path.abspath(os.path.join(os.path.dirname(__file__),data_path1))

data_path2='../data/a_neg'
neg= os.path.abspath(os.path.join(os.path.dirname(__file__),data_path2))

pickel_name='../data/normal_count_stop_final.pkl'
idf_pickle_name='../data/idf.pkl'
dict={}
dict['pos']=defaultdict(int)
dict['neg']=defaultdict(int)

idf=defaultdict(int)

sw=stopwords.words('english')
stopword={}
for i in sw:
    stopword[str(i)]=1

stemmer = PorterStemmer()

def parse(f,pol):
    for i in f:
        i = i.strip()
        
        if len(i) == 0:
            continue
        
        words = word_tokenize(i)
        id=words[0]
        words=words[1:]
        tIDF={}
        for word in words:
            
            if word.isalnum() or '-' in word:
                split_text =[ word ]
                if '-' in word:
                    split_text = word.split('-')
                    
                for k in split_text:
                    k=k.lower()
                    if k.isalpha() and not k in stopword:
                        #k=stemmer.stem(k)
                        tIDF[k]=1
                        dict[pol][k]=dict[pol][k]+1
                        
        for (k,v) in tIDF.items():
            idf[k]=idf[k]+1
                                
def createPickle(name,dict):
    fileObject = open(name,'wb') 
    pickle.dump(dict,fileObject)   
    fileObject.close()    

def createPickleWithIDf(name1,name2,dict1,dict2,total):
    fileObject = open(name1,'wb') 
    pickle.dump(dict1,fileObject)   
    fileObject.close()    
    dict3={}
  
    for (k,v) in dict2.items():
        idf=math.log(total*1.0/v)
        dict3[k]=idf
        
    fileObject = open(name2,'wb') 
    pickle.dump(dict3,fileObject)   
    fileObject.close()
    
def loadPickle(name):
    fileObject = open(name,'r')  
    b = pickle.load(fileObject)  
    print len(b)
        
fileObject = open(pos, 'r')  
text1 = fileObject.readlines()
parse(text1,'pos')

fileObject = open(neg,'r')  
text2 = fileObject.readlines()
parse(text2,'neg')

totaldocs=len(text1)+len(text2)

fileObject.close()

#createPickle(pickel_name, dict)
createPickleWithIDf(pickel_name, idf_pickle_name,dict,idf,totaldocs)
print('done')

'''
l=[]
[l.append((v,k)) for (k,v) in idf.items()]
l.sort(reverse=True)
for i in range(50):
    print l[i]
'''