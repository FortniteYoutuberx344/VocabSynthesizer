import docx
import requests
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfile

commonPath = "20k.txt"

gui = Tk()
gui.title("Vocab Synthesizer")
gui.geometry('1000x500') #width x height

# Create text widget and specify size.
T = Text(gui, height=100, width=100, yscrollcommand=set(), wrap=WORD)

# Create label
l = Label(gui, text="List of Uncommon Words in Text")
l.config(font=("Courier", 14))

path = ""
def open_file():
    global path
    file = askopenfile(mode='r')
    if file is not None:
        path = file

    defineWords()
    # state = disabled makes it uneditable (state defaults to normal)
    T.config(state=DISABLED)

btn = Button(gui, text ='Import a doc file', command = lambda:open_file())

def getText(path):
    doc = docx.Document(path)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

#creates a list of words from the text (all lower, no numbers, special characters)
def clean(string):
    text = string.lower()
    words = text.split()
    words = [word.strip('.,!;()[]') for word in words]
    words = [word.replace("'s", '') for word in words]
    words = [word for word in words if word.isalpha()]

    unique = []
    for word in words:
        if word not in unique and len(word) > 5:
            unique.append(word)

    unique.sort()
    return unique

def defineWords():
    docWords = clean(getText(path.name))

    common_file = open(commonPath, 'r')
    commonWords = clean(common_file.read())

    define = []
    for word in docWords:
        if word not in commonWords:
            define.append(word)
    print(len(define))

    #https://realpython.com/python-requests/
    wordNum = 1
    for word in define:
        wordDef =  str(wordNum) + ". " + word
        req = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        if (type(req.json()) is list):
            meanings = req.json()[0]['meanings']  # req.json is a list of length 1 with a dictionary inside
            partOfSpeech = meanings[0]['partOfSpeech']
            wordDef = wordDef + " (" + partOfSpeech + ") " + "\n"

            # meanings[0]['definitions'] is a list of dictionaries that can be any length
            for defnum in range(len(meanings[0]['definitions'])):
                definition = meanings[0]['definitions'][defnum]['definition']
                wordDef = wordDef + "   Definition " + str(defnum + 1) + ": " + definition + "\n"
                if ('example' in meanings[0]['definitions'][defnum]):
                    example = meanings[0]['definitions'][defnum]['example']
                    wordDef = wordDef + "   Example: " + example + "\n"

            T.insert(END, wordDef)
            T.insert(END, "\n")
            print("Inserting word " + str(wordNum))
        wordNum += 1

btn.pack()
l.pack()
T.pack()

gui.mainloop()

