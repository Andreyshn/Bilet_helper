from docx.shared import Pt
from docx import Document
import random as rnd
import time as t

class Question:
    def __init__(self,question,topic,importance):
        self.question = question # вопрос
        self.topic = topic #номер темы
        self.importance = importance #сложность

def main():
    d = []
    try:
        print("Введите количество билетов: ")
        N = int(input())
        print("Введите количество тем: ")
        m = int(input())
    except ValueError:
        print("Неправильный ввод")
        print("Пожалуйста, введите верное количество")
        return 1
    fullText = getText('voprosy.docx')
    my_doc = Document()
    i2 = 1  # Счетчик количества тем, добавленных в словарь
    i4 = 0 #Сложность вопроса
    for i in range(len(fullText)):
        if i + 1 == len(fullText) and i2 < m:
            print('''Заданного вами количества тем нет в файле
            Пожалуйста, исправьте документ, дописав темы
            Либо исправьте введенное количество''')
            return 1
        if fullText[i] == '':  # пустая строка - переход на другую тему
            i2 += 1
        else:
            try:
                i4 = int(fullText[i][-1])
                d.append(Question(fullText[i][:-1],i2,i4)) #сложность - последняя цифра вопроса
            except ValueError:
                i4 = 5
                d.append(Question(fullText[i],i2,i4)) #если сложность не задана - равна 5
    if m == i2:
        rdy = equality(d,i2,N) #равенство тем и вопросов в билете
    elif m > i2:
        rdy = more(d,i2,N) #тем больше вопросов



    return 0
def more(d,i2,N):
    pass
def equality(d,i2,N):
    rdy = ["Вопрос 0"]
    for i in range(1,i2+1):
            key = i 
            q = [obj.question for obj in d if obj.topic == i]
            imp = [obj.importance for obj in d if obj.topic == i]
            for j in range(N):
                key = generateTicket(q,imp,rdy,key,i)

def generateTicket(q,imp,rdy, key,key_copy):
    if key == 1:
        totalProbability = sum(imp)
        rnd_value = rnd.randint(1,totalProbability)
        cumulativeProbability = 0
        for i, prob in enumerate(imp):
            cumulativeProbability += prob
            if rnd_value <= cumulativeProbability:
                rdy.append(q[i])
                return key
    else:
        totalProbability = sum(imp)
        rnd_value = rnd.randint(1,totalProbability)
        cumulativeProbability = 0
        for i, prob in enumerate(imp):
            cumulativeProbability += prob
            if rnd_value <= cumulativeProbability:
                rdy.insert(key,q[i])
                return key+key_copy
def getText(filename):
    doc = Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return fullText

def formatDoc(doc):
    doc.styles['Normal'].font.name = 'Times New Roman'  # Название шрифта
    doc.styles['Normal'].font.size = Pt(12)  # Размер шрифта
    
main()