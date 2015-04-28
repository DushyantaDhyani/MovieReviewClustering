import os
import re
import math
from pandas import DataFrame as df

def getMovieName(filename):
    return filename.strip(".txt")

def getWordsInLine(line):
    return [word.strip().lower() for word in re.split(r'\W+',line) if word.strip().lower() not in StopList and len(word.strip())>0]

def getWordList(filepath):
    Words={}
    for line in open(filepath):
        words=getWordsInLine(line.strip())
        for word in words:
            if word in Words:
                Words[word]=Words[word]+1
            else:
                Words[word]=1
    return Words

StopList=set()
with open("StopWordsList.txt") as op:
    for line in op:
        StopList.add(line.strip().lower())
DataDir="wogmascrap/Data/"
GlobalWordsList={}
FileNames=os.listdir(DataDir)
NumberOfDocs=len(FileNames)
TfIdfMatrix=[]
DocWords={}
count=1
#FileNames=FileNames[1:40]
for filename in FileNames:
    filepath=DataDir+filename
    WordList=getWordList(filepath)
    DocWords[getMovieName(filename)]=WordList
    for word in WordList:
        if word not in GlobalWordsList:
            GlobalWordsList[word]=set([filename])
        else:
            GlobalWordsList[word].add(filename)
    count+=1
    if (count%100==0):
        print "Files Scanned "+str(count)

count=1
for filename in FileNames:
    DocCount=[]
    DocWord=DocWords[getMovieName(filename)]
    TotalFrequency=sum([value for value in DocWord.itervalues()])
    for word in GlobalWordsList:
        if word in DocWord:
            tf=DocWord[word]*1.0/TotalFrequency
            idf=math.log(abs(NumberOfDocs/len(GlobalWordsList[word])))
            DocCount.append(tf*idf)
        else:
            DocCount.append(0)
    TfIdfMatrix.append(DocCount)
    count+=1
    if (count%100==0):
        print "Files Processed "+str(count)



TfIdfMatrix=df(TfIdfMatrix,index=[getMovieName(filename) for filename in FileNames],columns=GlobalWordsList.keys())
TfIdfMatrix.index.name="MovieName"
TfIdfMatrix.to_csv("TfIdfData.csv",sep=",")