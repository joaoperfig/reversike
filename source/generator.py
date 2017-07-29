import speech_recognition as sr
from os import path
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

def test():
    tts = gTTS("blackbird", lang='en')
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
        


