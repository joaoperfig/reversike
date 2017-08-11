import speech_recognition as sr
from os import path
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
from mikerar_for_rev import memory
from mikerar_for_rev import wsort
import mikerar_for_rev as mikerar
import random

def test():
    tts = gTTS("Shay has grown harvested.", lang='en')
    tts.save("gtemp.mp3")    
    audio = AudioSegment.from_file("gtemp.mp3")
    audio = audio.reverse()
    play(audio)
    audio.export("gtemp.flac", format = "flac")
    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "gtemp.flac")
    r = sr.Recognizer()
    print(AUDIO_FILE)
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file   
        
    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        
# rselect RandomSelect returns random element of list
def rselect(lista):
    return random.choice(lista)


# wselect WeightedSelect returns element of dictionary based on dict weights {element:weight}
def wselect(dicti):
    total=0
    for i in list(dicti):
        total = total + dicti[i]
    indice = total*random.random()
    for i in list(dicti):
        if dicti[i]>=indice:
            return i
        indice = indice - dicti[i]
    raise ValueError ("something went wrong")
   
def tempFile():
    return "../temp/gtemp.mp3"
        
def flacFile():
    return "../temp/gtemp.flac"

def interpRev(sent):
    tts = gTTS(sent, lang='en')
    tts.save(tempFile())      
    audio = AudioSegment.from_file(tempFile())
    audio = audio.reverse()    
    audio.export(flacFile(), format = "flac")
    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), flacFile())
    
    r = sr.Recognizer()           #Generate the files for interpretation
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file     
        
    try:                          #Interpret through google's api
        interp = r.recognize_google(audio)
    except sr.UnknownValueError:
        interp = ""
    except sr.RequestError as e:
        interp = ""
        print("Could not request results from Google Speech Recognition service; {0}".format(e))        
    return interp
        
def runOnce():
    size = wselect({1:4, 2:5, 3:4, 4:3, 5:1})
    sent = mikerar.generateSent(size)
    try:
        interp = interpRev(sent) 
    except:
        print("something went poop")
        return (sent, "", "", 0)        
    if interp == "":
        return (sent, "", "", 0) #sentence, interpretation, reinterp score
    try:
        reinterp = interpRev(interp)
    except:
        print("something went poop")
        return (sent, "", "", 0)
    rescore = maxComScore(sent, reinterp)/len(sent)

    print(sent + " --> " + interp + " <-- " + reinterp + " # "+str(rescore))
    return (sent, interp, reinterp, rescore)
    
def iterateAndFile(count=10):
    print("Dont forget to change filename, ya doofus!")
    for i in range(count):
        this = runIterations(2000,40)
        f = open("../resources/itandf7_"+str(i)+".txt", "w")
        for j in this:
            f.write(j[0] + " -> " + j[1] + " <- " + j[2] + " #" + str(j[3])+"\n")
        f.close()
    
def runIterations(count=200, topsize=10):
    top = ()
    counter = 0
    for i in range(count):
        print(str((counter/count)*100) +"%")
        counter = counter+1
        res = runOnce()
        if res[3] > 0:
            put = False
            for i in range(len(top)):
                if res[3]>top[i][3]:
                    top = top[:i] + (res,) + top[i:]
                    put = True
                    break
            if not put:
                top = top + (res,)
            top = top[:topsize]
    return top
                
def maxComScore(sent1, sent2):
    if len(sent1) == 0 or len(sent2) == 0:
        return 0
    l = longestComSub(sent1, sent2)
    if len(l) == 0:
        return 0
    i1 = sent1.index(l)
    i2 = sent2.index(l)
    first1 = sent1[:i1]
    first2 = sent2[:i2]
    second1 = sent1[i1+len(l):]
    second2 = sent2[i2+len(l):]
    return len(l) + maxComScore(first1, first2) + maxComScore(second1, second2)
    
def longestComSub(s1, s2): #not my stuff, got it online
    m = [[0] * (1 + len(s2)) for i in range(1 + len(s1))]
    longest, x_longest = 0, 0
    for x in range(1, 1 + len(s1)):
        for y in range(1, 1 + len(s2)):
            if s1[x - 1] == s2[y - 1]:
                m[x][y] = m[x - 1][y - 1] + 1
                if m[x][y] > longest:
                    longest = m[x][y]
                    x_longest = x
            else:
                m[x][y] = 0
    return s1[x_longest - longest: x_longest]