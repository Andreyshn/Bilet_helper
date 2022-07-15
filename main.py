from docx import Document
import time
import random


def main():  # Главная функция
    d = {}
    try:
        print("Введите количество билетов: ")
        N = int(input())
        print("Введите количество тем: ")
        m = int(input())
        print("Выберите формат исходного документа.")
        print("1 - .docx \n2 - .txt")
        format = int(input())
    except ValueError:
        print("Неправильный ввод")
        print("Пожалуйста, введите верное количество")
        return 1
    if format != 2 or 1:
        print("Неверный ввод формата!")
        return 1
    if format == 1:
        fullText = getText('voprosy.docx')  # Работа с вопросами из docx
    else:
        fullText = getTxt('voprosy.txt')
    i2 = 1  # Счетчик количества тем, добавленных в словарь
    i3 = 1  # Счетчик вопросов в добавленной теме
    for i in range(len(fullText)):
        if i + 1 == len(fullText) and i2 < m:
            print("Заданного вами количества тем нет в файле")
            print("Пожалуйста, исправьте документ, дописав темы")
            print("Либо исправьте введенное количество")
            return 1
        if fullText[i] == '':  # проверка пустой строки
            if i2 == m:  # проверка достаточности тем
                print("Необходимое количество тем сформировано")
                break
            i2 += 1  # инкрементация счетчиков
            i3 = 1
        else:
            d[f'{i2}_{i3}'] = fullText[i]
            i3 += 1
        d[i2] = i3 - 1  # добавление в словарь счета вопросов каждой темы
    document = Document()  # Создание нового документа
    document.add_heading('Билеты', 0)  # Создание заголовка
    random.seed(time.time())
    for i in range(1, N + 1):  # Начало заполнения документа
        document.add_heading(f'Билет Номер: {i}', level=1)  # Добавление заголовка с номером билета
        if DocMake(document, m, d) == 1:  # функция, заполняющая основной документ
            return 1
    document.save('bilet.docx')  # Сохранение документа
    document = Document()  # Создание документа с невошедшими вопросами
    document.add_heading("Невошедшие вопросы", 0)
    for i2 in range(1, m + 1):
        document.add_heading(f'Тема {i2}')
        for i in range(0, d[i2]):
            name = f'{i2}_{i+1}'  # генерация имени
            document.add_paragraph(f'{d[name]}', style=f'List Bullet')  # постановка строки в документ
    document.save('non_bilet.docx')
    return 0


def DocMake(document, m, d):  # Функция для заполнения документов
    for i2 in range(1, m + 1):
        if d[i2] == 0:  # Преждевременный выход из цикла
            print("Закончились вопросы!")  # при случае нехватки вопросов
            print("Пожалуйста, добавьте недостающие вопросы в разделы.")
            return 1
        count = random.randint(1, d[i2])
        name = f'{i2}_{count}'  # сборка кодового значения по шаблону
        document.add_paragraph(f'{d[name]}', style=f'List Bullet')  # добавление самого билета
        d.pop(name)  # удаление использованного билета из словаря
        if count != d[i2]:
            name2 = f'{i2}_{d[i2]}'  # сборка названия максимального элемента
            d[name] = d[name2]
            d.pop(name2)
        d[i2] = d[i2] - 1  # скручивание счетчика количества


def getText(filename):  # Функция для чтения файла типа .docx
    doc = Document(filename)
    fullText = []
    for para in doc.paragraphs:  # Берем текст из параграфа и записываем его в строку
        fullText.append(para.text)
    return fullText

def getTxt(filename):
    fullText = []
    with open(f'{filename}') as f:
        for line in f:
            if line == '\n':
                fullText.append('')
            else:
                fullText.append(line)
    return fullText

if __name__ == "__main__":
    main()

