import pandas as pd
import operator
import random
import math
name1=""
name2=""
#Cosine Similarity Function to find the similarity between two feature vectors
def cosineSimilarity(doc1,doc2):
    dotprod=0
    mag1=0
    mag2=0
    for x,y in zip(doc1,doc2):
        try:
            dotprod+=x*y
            mag1+=pow(x,2)
            mag2+=pow(y,2)
        except:
            #print "Issues in Cosine Similarity"
            exit()
    mag1=math.sqrt(mag1)
    mag2=math.sqrt(mag2)
    return dotprod*1.0/(mag1*mag2)


def addPoints(vec1,vec2):
    return [(x+y) for x,y in zip(vec1,vec2)]

NumOfClusters=15
NumOfIter=20
data=pd.read_csv("TfIdfData.csv",index_col=0,header=0)
MovieNames=data.index
Centroids=data.ix[random.sample(data.index,NumOfClusters)]
CentroidAllocated=[None]*len(data)
centroid=0
similarity=0

for i in range(0,NumOfIter):
    print "Starting Iteration "+str(i+1)
    for j in range(0,len(MovieNames)):
        centroid=0
        moviedata=data.loc[MovieNames[j]].values.tolist()
        similarity=cosineSimilarity(moviedata,Centroids.iloc[0].tolist())
        for k in range(1,len(Centroids)):
            centroidtemp=Centroids.iloc[k]
            similaritytemp=cosineSimilarity(moviedata,centroidtemp.tolist())
            if similaritytemp>similarity:
                centroid=k
                similarity=similaritytemp
        CentroidAllocated[j]=centroid
        if j%50 ==0:
            print "Centroid Allocated for "+str(j)

    for j in range(0,NumOfClusters):
        total=[0.0]*len(data.columns)
        count=0
        for k in range(0,len(CentroidAllocated)):
            if CentroidAllocated[k]==j:
               total=addPoints(total,data.iloc[k])
               count+=1
        Centroids.iloc[j]=[(x*1.0/count) for x in total]


with open("Output.txt",'w') as op:
    for x in CentroidAllocated:
        op.write(str(x)+"\n")

Mapper={}
Counter={}

for x in range(0,NumOfClusters):
    Counter[x]=0

for x in range(0,NumOfClusters):
    Mapper[x]={}

words=[str(x) for x in data.columns]
for j in range(0,len(MovieNames)):
    moviedata=data.loc[MovieNames[j]]
    index=CentroidAllocated[j]
    Counter[index]+=1
    category_map=Mapper[index]
    for word in words:
        if word in category_map:
            category_map[word]+=moviedata[word]
        else:
            category_map[word]=moviedata[word]
    Mapper[index]=category_map

for x in range(0,NumOfClusters):
    total=Counter[x]
    for key in  Mapper[x]:
        Mapper[x][key]/=total



op=open("FinalResults.txt",'w')
for x in range(0,NumOfClusters):
    Temp=[]
    MyMap=Mapper[x]
    for y in MyMap:
        Temp.append((y,MyMap[y]))
    sorted_map=sorted(Temp,key=operator.itemgetter(1),reverse=True)
    sorted_map=sorted_map[1:10]
    op.write("Category "+str(x)+"\n")
    op.write("----------------------\n")
    op.write('\t'.join([p for p,q in sorted_map])+"\n")
    op.write("======================\n")
op.close()