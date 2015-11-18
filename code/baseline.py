import os
import pickle
import nltk
from nltk import word_tokenize
import math
from nltk.corpus import stopwords

data_path1='../data/testpos'
pos= os.path.abspath(os.path.join(os.path.dirname(__file__),data_path1))

data_path2='../data/testneg'
neg= os.path.abspath(os.path.join(os.path.dirname(__file__),data_path2))

data_path2='../data/normal'
norm= os.path.abspath(os.path.join(os.path.dirname(__file__),data_path2))

#pickel_name='../data/normal_count_stop.pkl'
pickel_name='../data/normal_count_stop_final.pkl'

idf_pickle_name='../data/idf.pkl'

total_pos=0
total_neg=0
vocab=0
    
fileObject = open(pickel_name,'r')  
b = pickle.load(fileObject)  
fileObject.close()

fileObject = open(idf_pickle_name,'r')  
idf = pickle.load(fileObject)  
fileObject.close()

    
posdict=b['pos']
negdict=b['neg']
stopword={}
    
def init():
    global total_neg,total_pos,vocab
    
    for (k,v) in negdict.items():
        total_neg=total_neg+v
        
    for (k,v) in posdict.items():
        total_pos=total_pos+v
        
    vocab=len(posdict)+len(negdict)    
    sw=stopwords.words('english')
    print "total_pos->"+str(total_pos)
    print "total_neg->"+str(total_neg)
    print "vocab->"+str(vocab)
    print ''
    
    for i in sw:
        stopword[str(i)]=1

def parse(f):
        words1=[]
        i = f.strip()
        
        if len(i) == 0:
            return (-1,-1)
        
        words = word_tokenize(i)
        id=words[0]
        words=words[1:]
        for word in words:
            if word.isalnum() or '-' in word:
                split_text =[ word ]
                if '-' in word:
                    split_text = word.split('-')
                    
                for k in split_text:
                    if k.isalpha():
                        k=k.lower()
                        words1.append(k)
        return (id,words1) 

def classify(id,words):
    #POS
    
    post_contri=0
    tags=nltk.pos_tag(words)
    
    for (word,tag) in tags:
        if word in stopword:
            continue
       
        word=word.lower()
        count=posdict[word] 
        #print(word+"->"+str(count))
        val = (1+count)*1.0/(total_pos+vocab)
        
                                
        val=math.log(val)
        val=math.fabs(val)
        post_contri = post_contri+val
    
    neg_contri=0
    #print ''

    for (word,tag) in tags:
        if word in stopword:
            continue     

                   
        word=word.lower()
        count=negdict[word] 
        #print(word+"->"+str(count))
        
        val = (1+count)*1.0/(total_neg+vocab)
        
        val=math.log(val)
        val=math.fabs(val)
        neg_contri = neg_contri+val     
    
    #print(str(post_contri)+","+str(neg_contri))    

    if post_contri < neg_contri:
        print ''+id+"\t"+"POS"
    else:
        print ''+id+"\t"+"NEG"
               
init()

fileObject = open(norm, 'r')  
text = fileObject.readlines()
for i in text:
    (a,b)=parse(i)
    classify(a, b)
fileObject.close()