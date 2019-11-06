import pandas as pd
from openpyxl import load_workbook
from selenium import webdriver 

link = 'https://www.pokupay.ru/partners'

def get_pokupay(): # Парсинг pokupay и сохранение результата в таблицу output.xlsx
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    browser = webdriver.Chrome('/Users/YuriiDubinin/Desktop/parser/driver/chromedriver', chrome_options=options)
    browser.get(link)
    result = {}
    count = 0
    for a in browser.find_elements_by_xpath('/html/body/div/div[4]/div/div/div/a'):
        result[count] = []
        result[count].append(a.get_attribute('href'))
        count += 1
    browser.quit

    final = pd.DataFrame.from_dict(result, columns=['Вебсайт'], orient='index')

    book = load_workbook('output.xlsx')
    with pd.ExcelWriter('output.xlsx', engine='openpyxl') as writer:
        writer.book = book
        writer.sheets = dict((ws.title, ws) for ws in book.worksheets)    
        final.to_excel(writer, 'Pokupay')  
        writer.save()     