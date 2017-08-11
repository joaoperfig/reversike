from gtts import gTTS
import os
from os import path
from pydub import AudioSegment
from pydub.playback import play
import speech_recognition as sr

def tempFile():
    return "../temp/temp.mp3"

def tempFile2():
    return "../temp/gtemp.mp3"
        
def flacFile():
    return "../temp/gtemp.flac"

def interpRev(sent):
    tts = gTTS(sent, lang='en')
    tts.save(tempFile2())      
    audio = AudioSegment.from_file(tempFile2())
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

class Sentence:
    def __init__(self, normal):
        self._normal = normal
        self._reverse = revth(normal)
        self._nosrev = revth(nospaces(normal))
        self._interp = ""
        
    def __repr__(self):
        return "#" + self._normal + "#"
    
    def show(self):
        print(self._normal)
        
    def showrev(self):
        print(self._reverse)
    
    def shownosrev(self):
        print(self._nosrev)
        
    def showinterp(self):
        print(self._interp)
        
    def say(self):
        tts = gTTS(text=self._normal, lang='en')
        tts.save(tempFile())
        audio = AudioSegment.from_file(tempFile())
        play(audio)
        
    def sayrev(self):
        tts = gTTS(text=self._reverse, lang='en')
        tts.save(tempFile())
        audio = AudioSegment.from_file(tempFile())
        play(audio)
        
    def revsay(self):
        tts = gTTS(text=self._normal, lang='en')
        tts.save(tempFile())
        audio = AudioSegment.from_file(tempFile())
        audio = audio.reverse()
        play(audio)    
        
    def sayinterp(self):
        tts = gTTS(text=self._interp, lang='en')
        tts.save(tempFile())
        audio = AudioSegment.from_file(tempFile())
        play(audio)    
        
    def sayrevinterp(self):
        tts = gTTS(text=self._interp, lang='en')
        tts.save(tempFile())
        audio = AudioSegment.from_file(tempFile())
        audio = audio.reverse()
        play(audio)    

def reverse(string):
    rev = ""
    for i in string:
        rev = i + rev
    return rev

def revth(string, avoids = ("th", "sh")): #reverse string without reversing elements in avoids
    for av in avoids:
        string = revsub(string, av)
    return reverse(string)

def revsub(string, sub):            #reverse instances of sub within string
    cuts = str.split(string, sub)
    final = ""
    for i in cuts:
        final = final + i + reverse(sub)
    final = final[:-len(sub)]
    return final

def nospaces(string):
    n = str.split(string, " ")
    new = ""
    for i in n:
        new = new + i
    return new

def interface():
    print("         __          __          __          __          __           ")
    print("      __/  \__    __/  \__    __/  \__    __/  \__    __/  \__    __  ")
    print("   __/  \     \__/  \     \__/  \     \__/  \     \__/  \     \__/  \ ")
    print("  /     /   __/     /   __/     /   __/     /   __/     /   __/     / ")
    print("  \__   \__/  \__   \__/  \__   \__/  \__   \__/  \__   \__/  \__   \ ")
    print("     \__/  \     \__/  \     \__/  \     \__/  \     \__/  \     \__/ ")
    print("   __/     /   __/     /   __/     /   __/     /   __/     /   __/    ")
    print("  /  \__   \__/  \__   \__/  \__   \__/  \__   \__/  \__   \__/  \__  ")
    print("  \     \__/  \     \__/  \     \__/  \     \__/  \     \__/  \     \ ")
    print("  /   __/     /   __/     /   __/     /   __/     /   __/     /   __/ ")
    print("  \__/        \__/        \__/        \__/        \__/        \__/    ")
    print("Welcome to the Reversike shell interface for doing cool stuff (check out Mew's 'Nervous')")
    print("Note that sentences are never saved by reversike, please write them somewhere!")
    mainMenu()
    
def mainMenu():
    while True:
        print("Ss - Start writing a sentence")
        print("Dd - Small reverse thingy database")
        print("Cc - Credits")
        print("Qq - Quit")        
        inp = input(">")
        if len(inp) == 0:
            print("Input, please")        
        elif inp in "Ss":
            sent = sentenceMenu()
            editMenu(sent)
        elif inp in "Dd":
            databaseMenu()
        elif inp in "Cc":
            creditMenu()
        elif inp in "Qq":
            return

def databaseMenu():
    print(open("database.txt", "r").read())

def creditMenu():
    print("Joao Figueira")

def sentenceMenu():
    while True:
        print("Input your initial sentence:")
        sent = input(">")
        while True:
            print("Is this sentence ok?: "+sent +" (Yy Nn)")
            inp = input(">")
            if len(inp) == 0:
                print("Input, please")            
            elif inp in "Yy":
                return Sentence(sent)
            elif inp in "Nn":
                break
            
def editMenu(sent):
    while True:
        print("Original        :"+sent._normal)
        print("Reverse bundled :"+sent._nosrev)
        print("Normal reverse  :"+sent._reverse)
        print("Interpretation  :"+sent._interp)
        print("Ee-editSent, Hh-editInterp, Ss-say, Rr-sayRev, Tt-revSay, Ii-sayInterp, Kk-sayRevInterp, Oo-autoInterp, Dd-database, Qq-quit")
        inp = input(">")
        if len(inp) == 0:
            print("Input, please")
        elif inp in "Ee":
            sent = editSentMenu(sent)
        elif inp in "Hh":
            sent._interp = editInterpMenu(sent._interp)
        elif inp in "Ss":
            sent.say()
        elif inp in "Rr":
            sent.sayrev()
        elif inp in "Tt":
            sent.revsay()
        elif inp in "Ii":
            sent.sayinterp()
        elif inp in "Kk":
            sent.sayrevinterp()     
        elif inp in "Oo":
            interp = interpRev(sent._normal)
            if interp == "":
                print("Automatic interpretation dectector could not find anything")
                print("Your old interpretation will not be replaced")
            else:
                print("Automatic interpretation detected:")
                print("          "+interp)
                sent._interp = interp
        elif inp in "Dd":
            databaseMenu()
        elif inp in "Qq":
            return
        
def editSentMenu(sent):
    while True:
        print("Current sentence: " + sent._normal)
        print("Write new sentence or Cc to cancel")        
        inp = input(">")
        if len(inp) == 0:
            print("Input, please")        
        elif inp in "Cc":
            return sent
        else:
            s = Sentence(inp)
            s._interp = sent._interp
            return s
        
def editInterpMenu(old):
    while True:
        print("Current interpretation: " + old)
        print("Write new interpretation or Cc to cancel")   
        inp = input(">")
        if len(inp) == 0:
            print("Input, please")        
        elif inp in "Cc":
            return old
        else:
            return inp     
        
interface()
        
            
        
        