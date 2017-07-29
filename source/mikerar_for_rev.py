import pickle
import gzip
import shutil
import os
import time

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

def transmike(filename):
    source = "transrar/hp1_en.pi"
    dest = "transrar/hp1_pt.pi"
    mems = getData(source)
    memd = getData(dest)
    f = open(filename, "r",  encoding="utf8")
    text = f.read()
    f.close()
    compressed = compressString(text, mems)
    text = decompressString(compressed, memd)
    f = open("translated_" + filename, "w",  encoding="utf8")
    f.write(text)
    f.close()    
    
def remike(filename):
    small = "remike_en/mikerar1.pi"
    large = "remike_en/mikerar2.pi"
    memsmall = getData(small)
    memlarge = getData(large)
    f = open(filename, "r",  encoding="utf8")
    text = f.read()
    f.close()
    compressed = compressString(text, memsmall)
    text = decompressString(compressed, memlarge)
    f = open("re" + filename, "w",  encoding="utf8")
    f.write(text)
    f.close()

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
    return "abcdefghijklmnopqrstuvwxyzçáàéèíìóòúùãõâêîôû"

def uppercase():
    return "ABCDEFGHIJKLMNOPQRSTUVWXYZÇÁÀÉÈÍÌÓÒÚÙÃÕÂÊÎÔÛ"

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
    

def decompress(filename):
    newname = filename.split(".")[0] + ".mkt"
    with gzip.open(filename, "rb") as f_in, open(newname, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    f = open(newname, "r", encoding="utf8") 
    compressed = f.read()
    f.close()
    os.remove(newname)
    newname2 = filename.split(".")[0] + ".txt"
    text = decompressString(compressed)
    f = open(newname2, "w",  encoding="utf8")
    f.write(text)
    f.close()

def decompressString(string, mem = getData()):
    print("decompressing")
    settings = possibleSettings()
    decompressed = ""
    lastword = "%#,start"
    jibber = ""
    number = ""
    st = ""
    wordserial = ""
    digitsleft = 0
    capitalize = False
    jibbering = False
    numbering = False
    wording = False    
    for i in string:
        if jibbering:
            if i == strLiteral():
                jibbering = False
                decompressed = decompressed + jibber
                jibber = ""
            else:
                jibber = jibber + i
        elif numbering:
            if i == intLiteral():
                numbering = False
                decompressed = decompressed + str(texttn(number))
                number = ""
            else:
                number = number + i
        elif wording:
            wordserial = wordserial + i
            digitsleft = digitsleft - 1
            if digitsleft == 0:
                wording = False
                print("finding serial:",wordserial)
                word = getWord(texttn(wordserial), st, lastword, capitalize, mem)
                if word == None:
                    print ("None Word ERROR!!! $$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                    word = word = mem._mainsort._list[0][0]
                decompressed = decompressed + word
                lastword = word
                st = ""
                wordserial = ""
                digitsleft = 0
                capitalize = False                  
        else:
            if i == strLiteral():
                jibbering = True
            if i == intLiteral():
                numbering = True
            if i in settings:
                wording = True
                sets = charSettings(i)
                #SerialType: specific, general   
                #Capitalize: no, yes
                #Space: no, left, right
                #Digit: no , . / ( ) " ' : ; - 
                #SerialDigits: no 1 2 3                
                if sets[0] == 0:
                    st = "specific"
                else:
                    st = "general"
                if sets[1] == 0:
                    capitalize = False
                else:
                    capitalize = True
                if sets[3] == 0:
                    digit = ""
                else:
                    print (sets)
                    print (i)
                    digit = inbetweeners()[sets[3]]
                if sets[2] == 0:
                    decompressed = decompressed + digit
                elif sets[2] == 1:
                    decompressed = decompressed + " " + digit
                else:
                    decompressed = decompressed + digit + " "
                digitsleft = sets[4]
                if digitsleft == 0:
                    wording = False
                    print("                 zero serial word!")
                    word = getWord(0, st, lastword, capitalize, mem)
                    decompressed = decompressed + word
                    lastword = word
                    st = ""
                    wordserial = ""
                    digitsleft = 0
                    capitalize = False                    
    return decompressed
            
def getWord(wordserial, st, lastword, capitalize, mem):
    print((wordserial, st, lastword, capitalize, mem))
    if st == "specific":
        if (wordserial < len(mem._wordsort[uncap(lastword)]._list)):
            word = mem._wordsort[uncap(lastword)]._list[wordserial][0]
        else:
            print(wordserial, "out of index of", lastword, " #########################")
            word = mem._wordsort[uncap(lastword)]._list[-1][0]
    elif st == "general":
        word = mem._mainsort._list[wordserial][0]
    else:
        raise ValueError ("invalid st:", st)
    print("getting word:", word)
    if capitalize:
        if (word[0] in lowercase()):
            return uppercase()[lowercase().index(word[0])] + word[1:]
        else:
            print("can't capitalize", word, " %%%%%%%%%%%%%%%%%%%%%%%%%")
            return word
    else:
        return word

def compress(filename, cut=False, size=0):
    tim = time.clock()
    delete = True
    f = open(filename, "r", encoding='utf8')
    text = f.read()
    f.close()
    if cut:
        text = text[:size]
    compressed = compressString(text)
    newname = filename.split(".")[0] + ".mkt"
    newname2 = filename.split(".")[0] + ".mkr"
    f = open(newname, "w", encoding="utf8")
    f.write(compressed)
    f.close()
    with open(newname, "rb") as f_in, gzip.open(newname2, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    if delete:
        os.remove(newname)
    tim2 = time.clock()
    timename = filename.split(".")[0] + "_" +str(tim2-tim).split(".")[0] + ".txt"
    print(timename)
    f = open(timename, "w", encoding="utf8")
    f.close()

def compressString(string, mem = getData()):
    compressed = ""
    lastword = "%#,start"
    thisword = ""
    thisnumber = ""
    inbetween = ""
    lastjibber = ""
    jibbering = True
    numbering = False
    wording = False
    for i in string:
        if jibbering:
            if i in lowercase() + uppercase():
                jibbering = False
                if (len(lastjibber) >= 2):
                    if lastjibber[-1] in inbetweeners():
                        if (lastjibber[-2] in inbetweeners()) and ((lastjibber[-2] in inbetweeners()[1:]) != (lastjibber[-1] in inbetweeners()[1:])):
                            inbetween = lastjibber[-2:]
                            lastjibber = lastjibber[:-2]
                        else:
                            inbetween = lastjibber[-1:]
                            lastjibber = lastjibber[:-1]
                elif (len(lastjibber) == 1):
                    if lastjibber in inbetweeners():
                        inbetween = lastjibber
                        lastjibber = ""
                compressed = compressed + strLiteral() + lastjibber + strLiteral()
                lastjibber = ""
                wording = True
                thisword = i
            elif i in numbers():
                jibbering = False
                compressed = compressed + strLiteral() + lastjibber + strLiteral()
                lastjibber = ""
                numbering = True
                thisnumber = i
            else:
                lastjibber = lastjibber + i
        elif numbering:
            if i in lowercase() + uppercase():
                numbering = False
                compressed = compressed + compressNumberString(thisnumber)   
                thisnumber = ""
                wording = True
                thisword = i
            elif i in numbers():
                thisnumber = thisnumber + i
            else:
                numbering = False
                compressed = compressed + compressNumberString(thisnumber)   
                thisnumber = ""
                jibbering = True
                lastjibber = i
        elif wording:
            if i in lowercase() + uppercase():
                thisword = thisword + i
            elif i in numbers():
                wording = False
                res = compressWordString(lastword, inbetween, thisword, mem)
                compressed = compressed + res[0]
                if(res[1]):
                    lastword = thisword
                thisword = ""
                inbetween = ""
                numbering = True
                thisnumber = i
            else:
                wording = False
                res = compressWordString(lastword, inbetween, thisword, mem)
                compressed = compressed + res[0]
                if(res[1]):
                    lastword = thisword
                thisword = ""
                inbetween = ""   
                jibbering = True
                lastjibber = i
        else:
            raise ValueError ("Invalid Booleans problem")
    if wording:
        compressed = compressed + compressWordString(lastword, inbetween, thisword, mem)[0]
    elif numbering:
        compressed = compressed + compressNumberString(thisnumber)
    elif jibbering:
        compressed = compressed + strLiteral() + lastjibber + strLiteral()
    else:
        raise ValueError ("Invalid Booleans problem 2")
    print()
    print(string)
    print(compressed)
    compressed = removeUnnecessaryLiterals(compressed)
    print(compressed)
    print()
    return compressed

def removeUnnecessaryLiterals(compressed):
    lista = compressed.split(strLiteral()*2)
    new1 = ""
    for i in lista:
        new1 = new1+i
    lista = new1.split(intLiteral()*2)
    new2 = ""
    for i in lista:
        new2 = new2+i
    return new2

def compressNumberString(string):
    index = 0
    while string[index] == "0":
        index = index + 1
        if index == len(string):
            return strLiteral() + string + strLiteral()
    zeroes = string[:index]
    number = string[index:]
    if len(number)<4:
        compnum = strLiteral() + number + strLiteral()
    else:
        compnum = intLiteral() + nttext(eval(number)) + intLiteral()
    return strLiteral() + zeroes + strLiteral() + compnum

def compressWordString(lastword, inbetween, thisword, mem):
    for i in thisword[1:]:
        if i in uppercase():
            return (strLiteral() + inbetween + thisword + strLiteral(), False)
    general = mem._mainsort.findIndex(uncap(thisword))
    if uncap(lastword) in list(mem._wordsort):
        specific = mem._wordsort[uncap(lastword)].findIndex(uncap(thisword))
    else:
        specific = None
       
    if (general == None): #nao existe
        print(thisword, "does not exist in data")
        return (strLiteral() + inbetween + thisword + strLiteral(), False)
    elif (specific == None): #so existe no general 
        print(thisword, "does not exist in", lastword +"'s", "data")
        return (createSettings(inbetween, thisword, general, "general"), True)
    else: #existe no specific
        print(thisword, "exists in", lastword +"'s", "data")
        return (createSettings(inbetween, thisword, specific, "specific"), True)
    
def createSettings(inbetween, word, serialid, serialtype):
    print((inbetween, word, serialid, serialtype))
    code = nttext(serialid)
    if (serialtype == "specific"):
        serial = 0
    elif (serialtype == "general"):
        serial = 1
    else:
        raise ValueError(serialtype + "is not a valid serial type")
    if (word[0] in lowercase()):
        capt = 0
    else:
        capt = 1
    if " " in inbetween:
        if len(inbetween) == 1:
            space = 1
            digit = 0
        elif inbetween[0] == " ":
            space = 1
            digit = inbetweeners().index(inbetween[1])
        else:
            space = 2
            digit = inbetweeners().index(inbetween[0])
    else:
        space = 0
        if len(inbetween) == 2:
            raise ValueError("no space in two digit inbetween")
        elif len(inbetween) == 1:
            digit = inbetweeners().index(inbetween)
        else:
            digit = 0
    sd = len(code)
    print(settingsChar(serial, capt, space, digit, sd) + code)
    return settingsChar(serial, capt, space, digit, sd) + code
    
#a Settings Character codes the following info about the upcoming word:
#SerialType: specific, general   
#Capitalize: no, yes
#Space: no, left, right
#Digit: no , . / ( ) " ' : \n - 
#SerialDigits: no 1 2 3
def settingsChar(serial, capt, space, digit, sd):
    base = 166
    a = 2
    b = 2
    c = 3
    d = 11
    e = 4
    return chr(base + serial*b*c*d*e + capt*c*d*e + space*d*e + digit*e + sd)

def charSettings(char):
    base = 166
    a = 2
    b = 2
    c = 3
    d = 11
    e = 4    
    order = ord(char)
    index = order - base
    sd = index%e
    index = index//e
    digit = index%d
    index = index//d
    space = index%c
    index = index//c
    capt = index%b
    index = index//b
    serial = index
    return (serial, capt, space, digit, sd)
    
def possibleSettings():
    string = ""
    for i in range(1+ ord(settingsChar(1, 1, 2, 10 ,3)) - ord(settingsChar(0, 0, 0, 0, 0))):
        string = string + chr(ord(settingsChar(0, 0, 0, 0, 0))+i)
    return string


#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
def cutforexp(size):
    filename = "exp/eng_news_2015_10K-sentences.txt"
    f = open(filename, "r", encoding = "utf8")
    text = f.read()
    f.close()
    text = text[:size]
    newname = filename[:-4] + "_" + (6-len(str(size)))*"0" + str(size) + ".txt"
    f = open(newname, "w", encoding = "utf8")
    f.write(text)
    f.close()
    
def bestseqs(count, leng = 8):
    mem = getData()
    for i in range(count):
        first = mem._mainsort._list[i][0]
        stri = first
        last = first        
        for j in range(leng):
            new = mem._wordsort[last]._list[0][0]
            last = new
            stri = stri + " " + new
        if not "the" in stri:
            print (stri)