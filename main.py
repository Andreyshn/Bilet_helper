from docx.shared import Pt
from docx import Document
import random as rnd
import time as t
from itertools import chain

from numpy import true_divide
from insert import ex, ins
class Question:
    def __init__(self,question,topic,difficulty):
        self.question = question # вопрос
        self.topic = topic #номер темы
        self.difficulty = difficulty #сложность
        self.used = 0 #сколько раз использован вопрос

def main():
    Ncase = 0
    d = [] #список списков объектов вопрос
    theme = [0.0] #список сложности тем
    try:
        print("Введите количество билетов: ")
        bilet_count = int(input())
        print("Введите количество вопросов в билете: ")
        theme_count = int(input()) #количество вопросов
    except ValueError:
        print("Неправильный ввод")
        print("Пожалуйста, введите верное количество")
        return 1
    
    full_text = getText('voprosy.docx')
    theme_in_doc= 1  # Счетчик количества тем, добавленных в словарь
    q_imp = 0 #Сложность вопроса
    count_q = 0 #счетчик вопросов каждой отдельной темы
    q = [] #список вопросов темы
    for i in range(len(full_text)):
        if full_text[i] == '':  # пустая строка - переход на другую тему
            if q != []:
                d.append(q)
            theme[theme_in_doc-1] /= count_q #среднее значение сложности темы
            theme_in_doc+= 1
            count_q = 0
            theme.append(0)
            q = [] #список вопросов темы
        else:
            try:
                q_imp = int(full_text[i][-1])
                q.append(Question(full_text[i][:-1],theme_in_doc,q_imp)) #сложность - последняя цифра вопроса
            except ValueError:
                q_imp = 5
                q.append(Question(full_text[i],theme_in_doc,q_imp)) #если сложность не задана - равна 5
            finally:
                theme[theme_in_doc-1] += q_imp
                count_q += 1
    d.append(q)
    theme[theme_in_doc-1] /= count_q #среднее значение сложности темы
    target_diff = int(sum(theme) / theme_in_doc * theme_count) #целевая сложность билета
    new_d = list(chain.from_iterable(d))
    if theme_count == theme_in_doc:
        Ncase = 1
    elif theme_count > theme_in_doc:
        Ncase = 2
        rnd.shuffle(new_d)
    else:
        Ncase = 3
    rdy = equality(new_d,theme_in_doc,theme_count,bilet_count,target_diff, Ncase)
    ins(rdy, theme_count)
    print(f'Сформировано: {len(rdy)} билетов') # type: ignore
    return 0



def equality(d,theme_in_doc,theme_count,bilet_count,target_diff, Ncase):
    rnd.seed(t.time())
    rdy = []
    i = 0
    step = 0
    allowed_rep = 1
    #rnd.shuffle(d)
    while i < bilet_count:
        bilet = algo(target_diff, theme_count, d, step, allowed_rep, Ncase)
        if len(bilet) < theme_count: # type: ignore
            print("Больше нет билетов с целевой сложностью")
            print("Произвожу увеличение цели")
            step += 1
            if target_diff - step == 0:
                print("Невозможно создать больше билетов!")
                break
            allowed_rep += 1
            if Ncase == 2: 
                rnd.shuffle(d)
        else:
            #print("Билет сформирован, попал под", target_diff, "+-", step)
            rdy.append(bilet)
            i += 1
    return rdy



def algo(target_diff, theme_count,d, step,allowed_rep, Ncase):
    current_diff = 0 #текущая сложность
    rdy = []
    i = 0
    themes = [-1] # повторение тем вопросов
    while i < len(d):
        if d[i].used < allowed_rep and foo(Ncase, d[i].topic, themes): #вопрос можно использовать(повторения и темы)
            current_diff += d[i].difficulty #проверяем сложность
            if current_diff <= target_diff + step: #если меньше/равен максимального порога
                if len(rdy)+ 1 == theme_count: #этот вопрос последний из необходимых
                    if current_diff == target_diff - step or current_diff == target_diff + step: #и он равен нашей цели
                        d[i].used += 1 #мы его используем
                        rdy.append(d[i].question) #добавляем
                        print("Билет сформирован, имеет сложность:", current_diff)
                        return rdy #завершаем прогонку
                    else: #он последний, но цели не равен
                        current_diff -= d[i].difficulty #убираем его из счета
                else: #вопрос не последний из необходимых, мы можем добавить еще
                    rdy.append(d[i].question) #мы добавляем ЕГО
                    themes.append(d[i].topic)
                    d[i].used += 1 #и используем
                    last_added = i #запоминаем его место, чтобы в случае чего бахнуть
            else: #мы превысили максимальный предел вопросов (использовав последний)
                current_diff -= d[i].difficulty #убираем его из счета
        else: #вопрос еще нельзя использовать
            pass
        try:
            if i + 1 == len(d) and len(rdy) < theme_count: #это последний вопрос в принципе, но нужно еще пройти
                i = last_added
                rdy.pop()
                themes.pop()
                d[i].used -= 1
                current_diff -= d[i].difficulty
            i += 1
        except IndexError:
            return []
        
    else:
        print("мы прошлись по всем вопросам")
        return []
    
def foo(*args):
    Ncase, q, themes = args
    if Ncase == 1:
        if q not in themes:
            return True
        else:
            return False
    else:
        if q != themes[-1]:
            return True
        else:
            return False


def getText(filename):
    doc = Document(filename)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return full_text

def formatDoc(doc):
    doc.styles['Normal'].font.name = 'Times New Roman'  # Название шрифта
    doc.styles['Normal'].font.size = Pt(12)  # Размер шрифта
    
main()
input("Для выхода нажмите Enter")