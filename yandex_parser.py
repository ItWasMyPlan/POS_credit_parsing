import pandas as pd
import urllib.parse
from bs4 import BeautifulSoup as bs
from selenium import webdriver  
from openpyxl import load_workbook


link_yandex = 'https://yandex.ru/search/ads?text='
default_exceptions = urllib.parse.quote(' -создание -продвижение -студия')


def get_content(link, type=True): #функиция эмулирующая браузер Хром и забирающая html код со страницы для дальнейших действий
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    browser = webdriver.Chrome('/Users/YuriiDubinin/Desktop/parser/driver/chromedriver', chrome_options=options)
    browser.implicitly_wait(3) #Обход блокировки
    browser.get(link)
    if type == True: # Сбор ссылок с Контактной информацией
        link_list = []
        for a in browser.find_elements_by_link_text('Контактная информация'):
            link_list.append(a.get_attribute('href'))
        browser.quit()
        return link_list
    else: # Парсинг данный со страницы Контактной информации
        content = []
        content.append(browser.find_element_by_xpath('//*[@id="title"]').text)
        content.append(browser.find_element_by_xpath('/html/body/div/div[3]/div/a').get_attribute('href'))
        try: 
            content.append(browser.find_element_by_xpath('/html/body/div/div[8]/div[2]/div[2]').text)
        except:
            content.append('N/a')
        try: 
            content.append(browser.find_element_by_css_selector('a.email').get_attribute('href')[7:])
        except:
            content.append('N/a')
        try: 
            content.append(browser.find_element_by_css_selector('div.contact-item:nth-child(1) > div:nth-child(2)').text)
        except:
            content.append('N/a')
        browser.quit()
        return content


def main_yandex(pages, search_text, sheet_name='Unnamed'): 
    result = {}
    count = 0
    text_request = urllib.parse.quote(search_text)
    for x in range(int(pages)):
        request = link_yandex + text_request + default_exceptions + '&p=' + str(x)
        link_list = get_content(request, True)
        for y in link_list:
            result[count] = get_content(y, False)
            result[count].append('Yandex Search')
            count += 1
    final = pd.DataFrame.from_dict(result, columns=['Название компании', 'Вебсайт', 'Номер телефона', 'e-mail', 'ОГРН/ОГРНИП', 'Источник информации'], orient='index')
    output = final.drop_duplicates(subset='Название компании')
    book = load_workbook('output.xlsx')
    with pd.ExcelWriter('output.xlsx', engine='openpyxl', options={'strings_to_urls': False}) as writer:
        writer.book = book
        writer.sheets = dict((ws.title, ws) for ws in book.worksheets)    
        output.to_excel(writer, sheet_name='Yandex_' + sheet_name)  
        writer.save()     