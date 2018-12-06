
import json
import requests


def readFile():
    word_list = []
    f = open("sample_list.txt", "r")
    for line in f:
        lines = line.strip('\r\n')
        word_list.append(lines)

    return word_list


def getNeighbors(word_list):
    url = 'http://ace.autotutor.org/aceapi2017/api/lsa'
    mydict = {}

    for w in word_list:
    	if not any(char.isdigit() for char in w):
            try:
                term = w
                data = json.loads('{"SpaceName":"English_TASA","Text1":"'+term+'","Count":"6","Task":"NN"}')
                Restresponse = requests.post(url, data=data)

                neigh = []

                for n in range(0, 6):
                    nerighborTerm = json.loads(Restresponse.text)['neighbors'][n]['term']
                    similarity = json.loads(Restresponse.text)['neighbors'][n]['similarity']

                    if n == 0:
                        word = nerighborTerm.encode('ascii')

                    else:
                        neigh.append([nerighborTerm.encode('ascii'), similarity])
                        #neigh.append(similarity)

                mydict[word] = neigh

            except Exception as error:
                print('Caught error: ' + w)
    return mydict


def write(mydict):
    f = open('output_similarity.txt', 'w')

    for a in mydict: #write the term
        f.write(a.decode("utf-8") + ": \n")

        for b in mydict[a]: #write neighbors and similarity
            f.write(b[0].decode("utf-8") + ", " + str(b[1]) + "\n")

        f.write("\n")

        

def main():
    l = readFile()
    n = getNeighbors(l)
    write(n)

    

main()

