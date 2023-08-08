from networktables import NetworkTables
from customtkinter import CTkTextbox
import customtkinter
import Levenshtein
import string
import time
import re


def sortTextAndIndexes(text, allowPeriods):
    if allowPeriods: textRegex = r'([^,]+(?:,|$))'
    else: textRegex = r'([^,]+)'
    textMatches = [(i.group(1).strip(), i.start()) for i in re.finditer(textRegex, text)]    
    if allowPeriods: cleanMatches = [(textItem.translate(str.maketrans('', '', string.punctuation.replace('.', ''))), index) for textItem, index in textMatches]
    else: cleanMatches = [(textItem.translate(str.maketrans('', '', string.punctuation)), index) for textItem, index in textMatches]
    return cleanMatches

def transformToQuotedString(str):
    words = str.split()
    quotedWords = [f"'{word}'" for word in words]
    finalStr = '(' + ', '.join(quotedWords) + ')'
    return finalStr

def restrictValues(entries):
    for entry in entries:
        keyEntry :customtkinter.CTkEntry = entry[0]
        valueEntry :customtkinter.CTkEntry = entry[1]
        type :str = entry[2]

        if type == 'Number' and re.sub(r"[^\d.]|(\.(?=.*\.))", "", valueEntry.get()) != valueEntry.get():
            text = valueEntry.get()
            valueEntry.delete(0, len(valueEntry.get()))
            valueEntry.insert(0, re.sub(r"[^\d.]|(\.(?=.*\.))", "", text))
        elif type == 'Boolean':
            text = valueEntry.get()
            if (('true'.__contains__(text.lower()) or 'false'.__contains__(text.lower())) == False and text != '') or text=='true' or text=='false':
                valueEntry.delete(0, len(valueEntry.get()))
                trueDist = Levenshtein.distance(text, 'true')
                falseDist = Levenshtein.distance(text, 'false')
                if trueDist < falseDist: valueEntry.insert(0, 'True')
                else: valueEntry.insert(0, 'False')
        elif type == 'Boolean[]':
            text = valueEntry.get()
            boolArr = sortTextAndIndexes(text=text, allowPeriods=False)
            for i in range(0, len(boolArr)):
                text = boolArr[i][0]
                index = boolArr[i][1]
                if (('true'.__contains__(text.lower()) or 'false'.__contains__(text.lower())) == False and text != '') or text=='true' or text=='false':
                    valueEntry.delete(index+1, index+1+len(text))
                    trueDist = Levenshtein.distance(text, 'true')
                    falseDist = Levenshtein.distance(text, 'false')
                    if trueDist < falseDist: valueEntry.insert(index+1, 'True')
                    else: valueEntry.insert(index+1, 'False')
            if valueEntry.get() == '':
                valueEntry.insert(0, '()')
            if valueEntry.get()[0] != '(':
                valueEntry.insert(0, '(')
            if valueEntry.get()[len(valueEntry.get())-1] != ')':
                valueEntry.insert(len(valueEntry.get()), ')')
        elif type == 'Number[]':
            text = valueEntry.get()
            rawArr = sortTextAndIndexes(text=text, allowPeriods=True)
            for i in range(0, len(rawArr)):
                text = rawArr[i][0]
                index = rawArr[i][1]
                if re.sub(r"[^\d.]|(\.(?=.*\.))", "", text) != text:
                    valueEntry.delete(index+1, index+1+len(text))
                    valueEntry.insert(index+1, re.sub(r"[^\d.]|(\.(?=.*\.))", "", text))
            if valueEntry.get() == '':
                valueEntry.insert(0, '()')
            if valueEntry.get()[0] != '(':
                valueEntry.insert(0, '(')
            if valueEntry.get()[len(valueEntry.get())-1] != ')':
                valueEntry.insert(len(valueEntry.get()), ')')
        elif type == 'String[]':
            text = valueEntry.get()
            for i in range(0, len(text)):
                if text[i] == ',' and text[i-1] != '\'' and text[i+1] != ' ' and text[i+2] != '\'':
                    text = text[:i] + "', '" + text[i+1:]
                    valueEntry.delete(0, len(valueEntry.get()))
                    valueEntry.insert(0, text)
                    i += 4
                    valueEntry.focus()
                    valueEntry.icursor(i)
            if valueEntry.get() == '':
                valueEntry.insert(0, '(\'\')')
            if valueEntry.get()[0] != '(':
                valueEntry.insert(0, '(')
            if valueEntry.get()[len(valueEntry.get()) -1] != ')':
                valueEntry.insert(len(valueEntry.get()), ')')
            if len(valueEntry.get()) > 1 and valueEntry.get()[1] != '\'':
                valueEntry.insert(1, '\'')
            if len(valueEntry.get()) > 1 and valueEntry.get()[len(valueEntry.get())-2] != '\'':
                valueEntry.insert(len(valueEntry.get())-1, '\'')
        elif type == 'Raw':
            text = valueEntry.get()
            rawArr = sortTextAndIndexes(text=text, allowPeriods=True)
            print(f'\n{rawArr}')
            for i in range(0, len(rawArr)):
                text = rawArr[i][0]
                index = rawArr[i][1]
                if re.sub(r'\D', '', text) != text:
                    valueEntry.delete(index+1, index+1+len(text))
                    valueEntry.insert(index+1, re.sub(r'\D', '', text))
            if valueEntry.get() == '':
                valueEntry.insert(0, '[]')
            if valueEntry.get()[0] != '[':
                valueEntry.insert(0, '[')
            if valueEntry.get()[len(valueEntry.get())-1] != ']':
                valueEntry.insert(len(valueEntry.get()), ']')

def unfocusedValues(entries):
    for entry in entries:
        valueEntry :customtkinter.CTkEntry = entry[1]
        type :str = entry[2]
        if type == 'Boolean':
            text = valueEntry.get()
            if (text.lower() != 'true' or text.lower() != 'false'):
                valueEntry.delete(0, len(valueEntry.get()))
                trueDist = Levenshtein.distance(text, 'true')
                falseDist = Levenshtein.distance(text, 'false')
                if trueDist < falseDist: valueEntry.insert(0, 'True')
                else: valueEntry.insert(0, 'False')    
        elif type == 'Boolean[]':
            text = valueEntry.get()
            boolArr = sortTextAndIndexes(text=text, allowPeriods=False)
            fixStr = '('
            for i in range(0, len(boolArr)):
                text = boolArr[i][0]
                index = boolArr[i][1]
                if text != 'True' and text != 'False':
                    trueDist = Levenshtein.distance(text, 'true')
                    falseDist = Levenshtein.distance(text, 'false')
                    if trueDist < falseDist: text = 'True'
                    else: text = 'False'
                if i != len(boolArr)-1: fixStr += (text + ', ')
                else: fixStr += (text + ')')
            valueEntry.delete(0, len(valueEntry.get()))
            valueEntry.insert(0, fixStr) 
        elif type == 'Number[]':
            text = valueEntry.get()
            text = re.sub(r'( *, *)+', ',', text)
            rawArr = sortTextAndIndexes(text=text, allowPeriods=True)
            fixStr = '('
            for i in range(0, len(rawArr)):
                text = rawArr[i][0]
                index = rawArr[i][1]
                if i != len(rawArr)-1:
                    tempStr = re.sub(r"[^\d.]|(\.(?=.*\.))", "", text)
                    if tempStr == '.': tempStr = '0.0'
                    fixStr += f'{str(float(tempStr))}, '
                else:
                    tempStr = re.sub(r"[^\d.]|(\.(?=.*\.))", "", text)
                    if tempStr == '.': tempStr = '0.0'
                    fixStr += f'{str(float(tempStr))})'
            valueEntry.delete(0, len(valueEntry.get()))
            valueEntry.insert(0, fixStr)
        elif type == 'String[]':
            text = valueEntry.get()
            words = text.split(',')
            cleanedWords = []
            print(f'\nWords: {words}')
            for word in words:
                firstSingleQuoteIndex = word.find('\'')
                secondSingleQuoteIndex = word.rfind('\'')
                word = word[firstSingleQuoteIndex + 1: secondSingleQuoteIndex]
                word = word.replace('\'', '')
                if word != '':
                    cleanedWords.append(word)
            print(f'Cleaned Words: {cleanedWords}')
            valueEntry.delete(0, len(text))
            valueEntry.insert(0, f'({str(cleanedWords)[1:len(str(cleanedWords))-1]})')
            if valueEntry.get() == '()':
                valueEntry.delete(0, 2)
                valueEntry.insert(0, '(\'\')')
        elif type == 'Raw':
            text = valueEntry.get()
            text = re.sub(r'( *, *)+', ',', text)
            rawArr = text.split(',')
            fixStr = '['
            cleanedBytes = []
            for i in range(0, len(rawArr)):
                text = rawArr[i]
                text = re.sub(r'\D', '', text)
                if text != '': cleanedBytes.append(text)
            for i in range(0, len(cleanedBytes)):
                text = cleanedBytes[i]
                if i != len(cleanedBytes)-1:
                    fixStr += f'{text}, '
                else: fixStr += f'{text}]'
            valueEntry.delete(0, len(valueEntry.get()))
            valueEntry.insert(0, fixStr)

def isTableEmtey(table):
    count :int = 0
    for key in table.getKeys():
        count+=1
    if count == 0: return True
    else: return False

preferences :any = []

#Initlialize and connect to Networktable
NetworkTables.initialize(server='localhost')
table = NetworkTables.getTable('SmartDashboard')
time.sleep(1.5)

#Initialize all the preferences inside a list
for key in table.getKeys():
    value = table.getValue(key=key, defaultValue=-1)
    type :str = ''
    if isinstance(value, float):
        type='Number'
    elif isinstance(value, str):
        type='String'
    elif isinstance(value, bool):
        type='Boolean'
        value=str(value)
    elif isinstance(value, tuple) and all(isinstance(i, float) for i in value):
        type='Number[]'
        value=str(value)
    elif isinstance(value, tuple) and all(isinstance(i, str) for i in value):
        type='String[]'
        value=str(value)
    elif isinstance(value, tuple) and all(isinstance(i, bool) for i in value):
        type='Boolean[]'
        value=str(value)
    elif isinstance(value, bytes):
        type='Raw'
        value=str([int.from_bytes(value[i:i+1], byteorder='big') for i in range(len(value))])
    else:
        type='Not Recognizable'
    preferences.append([key, value, type])

#Configure the window
customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')

window = customtkinter.CTk()
window.geometry('800x500')
window.resizable(False, False)
window.title('Networktable Preference Changer')

#Create tabs
tabView = customtkinter.CTkTabview(master=window)
tabView.pack(pady=10, padx=10, fill='both', expand=True)

tabView.add(name='Preferences')
tabView.add(name='Saves')
tabView.add(name="Settings")

#Configure the preferences tab
preferencesScrollableFrame = customtkinter.CTkScrollableFrame(master=tabView.tab('Preferences'), orientation='vertical', height=350)
preferencesScrollableFrame.pack(pady=10, padx=10, fill='x', anchor='n', expand=True)

addButton = customtkinter.CTkButton(master=tabView.tab('Preferences'), text='Add', width=250)
addButton.pack(padx=5, pady=10, side='left')
removeButton = customtkinter.CTkButton(master=tabView.tab('Preferences'), text='Remove', width=250)
removeButton.pack(padx=5, pady=10, side='left')
saveButton = customtkinter.CTkButton(master=tabView.tab('Preferences'), text='Save', width=250)
saveButton.pack(padx=5, pady=10, side='left')

def preferencesGUICreate():
    if (isTableEmtey(table) == False):
        keyLabel = customtkinter.CTkLabel(preferencesScrollableFrame, text='Key', font=('Arial', 12))
        keyLabel.grid(column=0, row=0)
        valueLabel = customtkinter.CTkLabel(preferencesScrollableFrame, text='Value', font=('Arial', 12))
        valueLabel.grid(column=1, row=0)
        typeLabel = customtkinter.CTkLabel(preferencesScrollableFrame, text='Type', font=('Arial', 12))
        typeLabel.grid(column=2, row=0)
    else:
        emteyLabel = customtkinter.CTkLabel(preferencesScrollableFrame, text='\n\n\n\n\n\t\tCouldn\'t find any preferences!\n\n\t\tSomething went wrong!', font=('Arial', 25))
        emteyLabel.grid(column=0, row=0)

    #Populate the preferences tab
    entries = []
    for i in range(2, len(preferences) + 2):
        key :str = preferences[i-2][0]
        value :str = preferences[i-2][1]
        type :str = preferences[i-2][2]

        keyEntry = customtkinter.CTkEntry(master=preferencesScrollableFrame, height=22, width=230, font=('Arial', 12))
        keyEntry.insert(0, key)
        keyEntry.grid(column=0, row=i, pady=5, padx=5)
        valueEntry = customtkinter.CTkEntry(master=preferencesScrollableFrame, height=22, width=230, font=('Arial', 12))
        valueEntry.insert(0, value)
        valueEntry.grid(column=1, row=i, pady=5, padx=5)
        typeLabel = customtkinter.CTkLabel(master=preferencesScrollableFrame, height=22, width=230, font=('Arial', 12), text=type)
        typeLabel.grid(column=2, row=i, pady=5, padx=5)

        entries.append([keyEntry, valueEntry, type])

        #Add saftey to entries so that invalid values are not set
        valueEntry.bind('<KeyRelease>', lambda event: restrictValues(entries))

    for entry in entries:
        keyEntry :customtkinter.CTkEntry = entry[0]
        valueEntry :customtkinter.CTkEntry = entry[1]
        valueEntry.bind("<FocusOut>", lambda event: unfocusedValues(entries))


preferencesGUICreate()

window.mainloop()