import xml.dom.minidom
import nltk
import numpy as np
import numpy
from sys import argv
from nltk.util import bigrams
from nltk.util import trigrams
from nltk import word_tokenize
import jellyfish
from jellyfish import jaro_distance
import collections
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
import scipy.spatial.distance as ssd
from lxml import etree

from scipy.cluster.hierarchy import fcluster



dictionary = collections.OrderedDict()
unigramDict = collections.OrderedDict()

def xmlParse(fileName):
      
    parser = etree.XMLParser(encoding='utf-8',recover=True)
    tree = etree.parse(fileName,parser);
        
        #Get all the instance tags
        #instances = collection.getElementsByTagName("instance")
    instances = tree.xpath('//instance')
        #Create an instance list 
    instanceList = list()
    #fwriter = open(answerKeyFileName,"w",-1,"utf-8")
        #Step through all the instance nodes in the xml file, which is in the senseval-2 format.
    for instance in instances:
            #Create an Instance object to hold all the data from the xml node
        #inst = Instance.Instance()
        #text = ""
        #rawText = ""
            #Get the instance id from the node and set the Instance objects instanceID
        inst.instanceID = instance.attrib["id"]
            
            #Get the answer information for auto generating the key file
        answer = instance[0]
        senseid = answer.attrib["senseid"]

            #Get the context node from the instance
        type = instance[1]

            #Get the head node
        headEl = type[0]

            #Using xpath get the text before the head node
        for item in headEl.xpath("preceding-sibling::*/text()|preceding-sibling::text()"):
            text += item.strip()
            rawText += item.strip()

            #Get the head nodes text (for example <head>light</head> you would get "light"), we also preserve the head tag in the rawText
        text +=  " " + headEl.text + " "
        rawText += " <" + headEl.tag + ">"
        rawText += headEl.text
        inst.head = headEl.text
        rawText += "</" + headEl.tag + "> "

            #Using xpath get the text after the head node
        for item2 in headEl.xpath("following-sibling::*/text()|following-sibling::text()"):
            text += item2.strip()
            rawText += item2.strip()
            
            #Set the Instance objects text to string retrieved from the context
        inst.text = text
        inst.rawText = rawText
            #Add the populated Instance object to the instanceList
        instanceList.append(inst)
            #Create and write out the key file

        #fwriter.write(inst.head + " " + str(inst.instanceID) + " " + str(senseid) + "\n")
    #fwriter.close()
    return instanceList


xmlParse(argv[1])


# This instance_dictionary maps to key-value pairs of instances.
# key is the instance id and the value is the context of instance.
# All the key-value pairs will be stored in dictionary

def instance_dictionary():
 
   keyfile = open("outputUse.txt", "r")
   key = 0;
   for line in keyfile:
      if(len(str(line)) >80):
           		dictionary[key] = line
           		key = key + 1;
      
instance_dictionary();

def unigram_dictionay():	
	
	fwriter=open("unigram.txt","w",-1,'utf-8')	
	instance = dictionary.items()
	for key, value in instance:
		tokens = nltk.word_tokenize(value)
		a = list(tokens)
		unigramDict[key] = a
	fwriter.write(str(unigramDict))				
	fwriter.close()

unigram_dictionay();


def compare(list_i, list_j):
	common = set(list_i) & set(list_j);
	return common;	
	
def distance(a,b):
	if(a>b):
		return a-b;
	else:
		return b-a;
		
		
def min(a,b):
	if(a>b):
		return a;
	else:
		return b;
		
		
def merge(x, y, table):
	for i in range(len(table)):
		table[i][x] = min(table[i][x], table[i][y])				
		table[x][i] = min(table[x][i], table[y][i])	
		
	temp_Table=numpy.array(table)
	#the next line deletes the row with index 'y'
	temp_Table=numpy.delete(temp_Table, y, axis =0)
	#the next line deletes the column with index 'y'
	temp_Table=numpy.delete(temp_Table, y, axis =1)
	temp_Table[x][x] = 0
	return temp_Table;
	
def updateInClusterList(x,y ,dictionaryTemp):

	items = list(dictionaryTemp.items())
	print(str(len(items)))
	clusterX = items[x][1];
	#items[x] gives the key-value pair at index 'x', 
	# as we just need the value, we take items[x][1]
	clusterY = items[y][1];
	keyToBeRemoved = items[y][0];
	for i in clusterY:		
		clusterX.append(i);
	#print(str(clusterX))
	#print(str(clusterY))
	del dictionaryTemp[keyToBeRemoved]
	return dictionaryTemp;

			
def count_commonBigrams():

	dict = {};
	instance = dictionary.items()
	fwriter1=open("list.txt","w",-1,'utf-8')
	
	i=0;
	while(i < len(instance)):
		clust = [];
		clust.append(i);
		dict[i] = clust;
		i=i+1;
	length = len(instance)
	
	# table stores jaro-distance of instances
	table= [ [ 0 for i in range(length) ] for j in range(length) ]
	tableScipy = table;
	d1=0;
	while(d1 < length):
		d2 = d1 + 1;
		while(d2 < length):
			#table[d1][d1] = 0
			#table[d2][d2] = 0;
			tempFreq = compare(unigramDict[d1],unigramDict[d2]);	
			table[d1][d2] = len(tempFreq)
			#table[d1][d2]= round(1 - jaro_distance(dictionary[d1],dictionary[d2]), 4)
			#table[d1][d2] = jellyfish.levenshtein_distance(dictionary[d1],dictionary[d2])
			table[d2][d1] = table[d1][d2];
			d2 = d2 +1;
		d1 = d1 + 1;
	fwriter1.write(str(table))		
	fwriter1.write("\n")		

	
	k=0;
	while(k < length-4):
		lowestPair = (0,1);
		lowest = distance(table[0][0] , table[0][1]);
		for i in range(len(table)):
			for j in range(i+1, len(table)):
				temp_lowDist = distance(table[i][i], table[i][j])
				if(temp_lowDist > lowest):
					lowest = temp_lowDist;
					lowestPair = (i,j)
		
		#fwriter1.write(str(lowest))
		#fwriter1.write(str(lowestPair))	
		#fwriter1.write("\n")
		#fwriter1.write(str(dict))	
		table = merge(lowestPair[0] , lowestPair[1], table)
		dict = updateInClusterList(lowestPair[0], lowestPair[1], dict);	
		#fwriter1.write(str(table))
		
		k = k+1;		
		
	#fwriter1.write(str(lowest))
	#fwriter1.write(str(lowestPair))
	fwriter1.write("\n")
	fwriter1.write(str(dict))
	#fwriter1.write(str(table))
	
			

	fwriter1.close()

count_commonBigrams();

