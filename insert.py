from hmac import new
from xml.dom.minidom import Element
from docx import Document
'''
ex() выполняет роль поиска таблицы из шаблона
и записывает ее в header_table
После этого fill() выделяет секцию документа, из секции заголовок
И вставляет туда таблицу напрямую
После этого записывает вопросы из готового списка(сейчас реализовано 3 вопроса)
Далее идет разрыв страницы
'''
def ex(doc):
    for elem in doc.element.body:
        if elem.tag.endswith('tbl'):
            return elem
    else:
        print('Неверный формат шаблонного документа!')
        return 1
    
def fill(rdy, theme_count, header_table, newDoc):
    section = newDoc.sections[0]
    header = section.header     
    header._element.append(header_table)
    for i in range(2, len(rdy), 3):
        newDoc.add_paragraph('\n')
        for j in range(i-2,i+1):
            newDoc.add_paragraph(f'{(j)%3+1}. {rdy[j]}')
        newDoc.add_page_break()
        newDoc.save('ready.docx')

def ins(rdy, theme_count):
    temp = Document('template.docx')
    newDoc = Document()
    header_table = None
    header_table = ex(temp)
    fill(rdy, theme_count, header_table, newDoc)