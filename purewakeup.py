import speech_recognition as sr
import pyaudio
import wave
import time

import playmusic, playvideo, texttoimage, texttoaudio

# Set recording parameters (adjustable)
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5

# Define wake word
WAKE_WORD = "hey"  # Replace with your desired wake word

# Initialize the Google Speech Recognition recognizer
r = sr.Recognizer()

def listen_for_wake_word():
    start = time.time()

    """Listens for the wake word using Google Speech Recognition."""
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source, phrase_time_limit=RECORD_SECONDS)

    try:
        transcription = r.recognize_google(audio)
        print(transcription)

        if WAKE_WORD.lower() in transcription.lower():
            end = time.time()
            print(end - start)
            return transcription
            #return True
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    end = time.time()
    print(end - start)

    return False

def record_audio():
    """Records audio after wake word detection."""
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print("Recording...")
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("Finished recording.")
    stream.stop_stream()
    stream.close()
    p.terminate()
    return frames

def save_audio(frames, filename="output.wav"):
    """Saves recorded audio to a WAV file."""
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(2)
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print(f"Audio saved to {filename}")
    
def remove_words(sentence):
    words_to_remove = ["hey", "genius"]
    word_list = sentence.split()
    new_word_list = [word for word in word_list if word.lower() not in words_to_remove]
    new_sentence = " ".join(new_word_list)
    return new_sentence

def queryengine(query):
    #query = "generate image for humans in mars"
    if "play song".lower() in query.lower():
        playmusic.main(query)
    elif "play video".lower() in query.lower():
        playvideo.main(query)
    elif "generate image".lower() in query.lower():
        texttoimage.main(query)
    elif "generate audio".lower() in query.lower():
        texttoaudio.main(query)
    


def has_alphabets(string):
    for char in string:
        if char.isalpha():
            return True
    return False


def main():
    while True:
        transcription = listen_for_wake_word()
        
        if transcription:
            print(transcription)
            query = remove_words(transcription)
            print(query)
            
            if has_alphabets(query):
                queryengine(query)
            else:
                print("Tell me action")
            

            

        #if listen_for_wake_word():
            #recorded_frames = record_audio()
            #filename = input("Enter filename (or press Enter for default): ") or "output.wav"
            #save_audio(recorded_frames, filename)
            #break  # Exit after recording

if __name__ == "__main__":
    main()