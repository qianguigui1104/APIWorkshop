
# this file gets the top 'n' nearest neighbors
# from the LSA API

import json
import requests


def readFile():	
#get the word list from a text file
    word_list = []
    f = open("sample_list.txt", "r")

    for line in f:
        lines = line.strip('\r\n')
        word_list.append(lines)

    return word_list


def getNeighbors(word_list): 
#get the nearest neighbors from the API

    url = 'http://ace.autotutor.org/aceapi2017/api/lsa'
    #the URL of the API

    mydict = {}

    for word in word_list:
        try:
        	text1 = word
        	data = json.loads('{"SpaceName":"English_TASA","Text1":"'+text1+'","Count":"5","Task":"NN"}')
        	Restresponse = requests.post(url, data=data)
        	top_neighbors = []

        	for n in range(0, 6):
        		nerighborTerm = json.loads(Restresponse.text)['neighbors'][n]['term']
        		if n != 0:
        		#appending top neighbors of the target word 
        			term = nerighborTerm.encode('ascii')
        			top_neighbors.append(term)

        	mydict[word] = top_neighbors

        except Exception as error:
            print('Caught error: ' + word)
    
    return mydict


def write(mydict):
    f = open('output.txt', 'w')

    for word in mydict: #write the term
        f.write(word + ": \n")

        for neighbors in mydict[word]: #write neighbors and similarity
            f.write(neighbors.decode("utf-8") + "\n")

        f.write("\n")

        

def main():
    l = readFile()
    n = getNeighbors(l)
    write(n)

    

main()

