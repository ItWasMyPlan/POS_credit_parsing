import requests as req
import pandas as pd
from bs4 import BeautifulSoup as bs
from openpyxl import load_workbook

link = 'https://shop.paylate.ru/tools/partners_page.php?SHOWALL_1=1&amp;count=36'

def get_paylate(): # Парсинг paylate и сохранение результата в таблицу output.xlsx
    soup = bs(req.get(link).text, "html.parser")
    div = soup('div', {'class': 'partner-part'})
    result = {}
    count = 0
    for x in div: 
        result[count] = []
        result[count].append(x.find('div', {'class': 'partner-text'}).getText().strip('\n'))
        result[count].append(x.find_all('a')[0].get('href'))
        count += 1

    final = pd.DataFrame.from_dict(result, columns=['Название компании', 'Вебсайт'], orient='index')

    book = load_workbook('output.xlsx')
    with pd.ExcelWriter('output.xlsx', engine='openpyxl') as writer:
        writer.book = book
        writer.sheets = dict((ws.title, ws) for ws in book.worksheets)    
        final.to_excel(writer, 'Paylate')  
        writer.save()     