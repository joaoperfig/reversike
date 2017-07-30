import pickle
import gzip
import shutil
import os
import time
import random

class wsort:
    def __init__(self):
        self._list = []
    def findIndex(self, word):
        for i in range(len(self._list)):
            if self._list[i][0]==word:
                return i
        return None
    def incIndex(self, word):
        i = self.findIndex(word)
        if i==None:
            self._list = self._list + [(word, 1)]
        else:
            self._list[i] = (word, self._list[i][1]+1)
            self.autoSort(i)
    def autoSort(self, index):
        value = self._list[index][1]
        while index > 0:
            if self._list[index-1][1] < value:
                carry = self._list[index-1]
                self._list[index-1] = self._list[index]
                self._list[index] = carry
                index = index-1
            else:
                return
    def toDict(self):
        dic = {}
        for i in self._list:
            dic[i[0]] = i[1]
        return dic
    def wselect(self): #faster than wselect(toDict(wsort))
        count = 0
        for i in self._list:
            count = count + i[1]
        selecter = count*random.random()
        for i in self._list:
            if i[1] >= selecter:
                return i[0]
            selecter = selecter-i[1]
        raise ValueError("Somethin went wrong")

class memory:
    def __init__(self):
        self._mainsort = wsort()
        self._wordsort = {}
    def learnWord(self, first, second):
        if first == None:
            first = "%#,start"
        else:
            first = uncap(first)
        second = uncap(second)
        self._mainsort.incIndex(second)
        if first in list(self._wordsort):
            self._wordsort[first].incIndex(second)
        else:
            new = wsort()
            new.incIndex(second)
            self._wordsort[first] = new
            
def generateSent(size, returnList = False):
    data = getData()
    last = data._wordsort["%#,start"].wselect()
    words = (last,)
    while len(words)<size:
        try:
            last = data._wordsort[last].wselect()
        except:
            last = data._mainsort.wselect()
        words = words + (last,)
    if returnList:
        return words
    string = words[0][0].capitalize() + words[0][1:]
    for i in words[1:]:
        string = string + " " + i
    string = string + "."
    return string
    

def uncap(word):
    return (" " + word).capitalize()[1:]

def getData(name = "mikerar.pi"):
    f = open(name, "rb")
    mem = pickle.load(f)
    f.close()
    return mem

def updateData(mem, name="mikerar.pi"):
    f = open(name, "wb")
    pickle.dump(mem, f)
    f.close()
    return

def tempData(mem):
    f = open("temprar.pi", "wb")
    pickle.dump(mem, f)
    f.close()
    return    

def getTData():
    f = open("temprar.pi", "rb")
    mem = pickle.load(f)
    f.close()
    return mem    

def learnSentence(sentence, mem):
    for i in range(len(sentence)):
        if sentence[i] in (" ,:_;/()[]{}\n-.?!'\t" + '"'):
            sentence = sentence[:i] + " " + sentence[i+1:]
    lista = sentence.split()
    if len(lista) == 0:
        return mem
    mem.learnWord(None , toLower(lista[0]))
    for i in range(len(lista)-1):
        mem.learnWord(lista[i], lista[i+1])
    return mem

def readBook(textfile, destmem, sourcemem = None):
    f = open(textfile, "r",encoding="cp1252", errors='ignore')
    text = f.read()
    f.close()
    lista = [text]
    for i in ".!?":
        nova = []
        for j in lista:
            nova = nova + j.split(i)
        lista = nova
    print(lista)
    total = len(lista)
    count = 0
    if (sourcemem == None):
        sourcemem = memory()
    else:
        sourcemem = getData(sourcemem)
    for line in lista:
        print(count*100/total, "%")
        count = count+1
        print((line, sourcemem))
        learnSentence(line, sourcemem)
    updateData(sourcemem, destmem)
    return

def parseWort(filename):
    f = open(filename, "r",encoding="utf8")
    lines = f.readlines()
    f.close()
    mem = getData()
    tempData(mem)
    total = len(lines)
    count = 0
    for line in lines:
        print(count*100/total, "%")
        count = count+1
        if "\t" in line:
            line = line.split("\t")[1][:-1]
        learnSentence(line, mem)
    updateData(mem)

def quickSort(alist):
    quickSortHelper(alist,0,len(alist)-1)

def quickSortHelper(alist,first,last):
    if first<last:
        splitpoint = partition(alist,first,last)
        quickSortHelper(alist,first,splitpoint-1)
        quickSortHelper(alist,splitpoint+1,last)

def partition(alist,first,last):
    pivotvalue = alist[first][1]
    leftmark = first+1
    rightmark = last
    done = False
    while not done:
        while leftmark <= rightmark and alist[leftmark][1] <= pivotvalue:
            leftmark = leftmark + 1
        while alist[rightmark][1] >= pivotvalue and rightmark >= leftmark:
            rightmark = rightmark -1
        if rightmark < leftmark:
            done = True
        else:
            temp = alist[leftmark]
            alist[leftmark] = alist[rightmark]
            alist[rightmark] = temp
    temp = alist[first]
    alist[first] = alist[rightmark]
    alist[rightmark] = temp
    return rightmark

def test():
    for i in range(100):
        print(i, ntd(i), dtn(ntd(i)))
        
def testt(n):
    for i in range(n):
        print(i+1, chr(i))

def dtn(digit):
    order = ord(digit)
    if (order <= 31) or ((order >= 127) and (order <= 160)) or (order >= 166):
        raise ValueError(digit+" is not a number digit")
    if (order < 127):
        return order - 32
    else:
        return order - 66

def ntd(number):
    if number >= 100:
        raise ValueError("ntd is for two digit numbers")
    if number <= 94:
        return chr(number+32)
    else:
        return chr(number+66)

def texttn(text):
    number=0
    for i in text:
        number = number*100 + dtn(i)
    return number

def nttext(number):
    string = ""
    while number != 0:
        string = ntd(number % 100) + string
        number = number//100
    return string

def strLiteral():
    return chr(694)

def intLiteral():
    return chr(695)

def inbetweeners():
    return " ,./()" + '"' +"':\n-"

def lowercase():
    return "abcdefghijklmnopqrstuvwxyz"

def uppercase():
    return "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def numbers():
    return "0123456789"

def toLower(word):
    new = ""
    for i in word:
        if i in uppercase():
            new = new + lowercase()[uppercase().index(i)]
        else:
            new = new + i
    return new
    

