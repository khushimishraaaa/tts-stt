from flask import Flask, render_template, request
import pyttsx3
import speech_recognition as sr

app = Flask(__name__)

def text_to_speech(text, voice_id='default'):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    if voice_id == 'male':
        engine.setProperty('voice', voices[0].id)
    elif voice_id == 'female':
        engine.setProperty('voice', voices[1].id)

    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    engine.say(text)
    engine.runAndWait()

def speech_to_text():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Speak something...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand the audio.")
        return ""
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tts', methods=['POST'])
def tts():
    text_input = request.form['text_input']
    voice_choice = request.form['voice_choice']

    text_to_speech(text_input, voice_choice)
    return render_template('index.html', message=f'Text "{text_input}" spoken successfully.')

@app.route('/stt')
def stt():
    result = speech_to_text()
    return render_template('index.html', stt_result=result)

if __name__ == '__main__':
    app.run(debug=True)
