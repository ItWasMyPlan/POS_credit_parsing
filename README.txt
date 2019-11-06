Required software:
ChromeDriver 78.0.3904.70 
Google Chrome Version 78.0.3904.70 (Official Build) (64-bit)
NOTE: Версии ChromeDriver и Google Chrome должны быть одинаковые!

Required libraries:
smtplib
os.path
email
email.mime
email.utils
selenium
BeautifulSoup4
pandas
openpyxl
schedule
time

Для корректной работы скрипта, необходимо исправить путь к ChromeDriver в yandex_parser.py  (15 строка) на реальный путь на вашем ПК. 

Принцип работы скрипта:
Данный скрипт парсит сайты конкурентов, а также выдачу Яндекс рекламы по определенным запросу. Скрипт работает циклично и раз в указанное количество дней повторяет запрос и заново высылает информацию на указанную почту.
