import pyttsx3

engine = pyttsx3.init()
engine.setProperty('voice', 'it-it')  # Set the language to US English
# Set the speaking rate to a slower speed
engine.setProperty('rate', 130)

text = 'siamo noi a lavorare per raggiungerli?'

engine.say(text)
engine.runAndWait()


engine = pyttsx3.init()

voices = engine.getProperty('voices')
for voice in voices:
    print('---------------------')
    print('ID:', voice.id)
    print('Name:', voice.name)
    print('Languages:', voice.languages)
    print('Gender:', voice.gender)