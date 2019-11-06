import paylate_parser as pay
import yandex_parser as ya
import smtplib
import schedule
import time
import os.path as op
import pokupay_parser as pp
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders

def send_mail(send_from, send_to, subject, message, files=[],
              server="localhost", port=587, username='', password='',
              use_tls=True):
    """
    Функция отправляющая результирующую таблицу на указанный e-mail
    Args:
        send_from (str): from name
        send_to (str): to name
        subject (str): message title
        message (str): message body
        files (list[str]): list of file paths to be attached to email
        server (str): mail server host name
        port (int): port number
        username (str): server auth username
        password (str): server auth password
        use_tls (bool): use TLS mode

    """
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(message))

    for path in files:
        part = MIMEBase('application', "octet-stream")
        with open(path, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="{}"'.format(op.basename(path)))
        msg.attach(part)

    smtp = smtplib.SMTP(server, port)
    if use_tls:
        smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()


def main(): # Фукнция управляюшая всем скриптом. В её тело можно добавить новые вызовы методов при необходимости.
    pay.get_paylate() # Парсим paylate
    pp.get_pokupay() # Парсим pokupay
    ya.main_yandex(10, 'интернет-магазин обуви', 'Обувь')   # Функция main_yandex принимает три аргумента: количество
    ya.main_yandex(10, 'турагенства', 'Турагенства')        # страниц выдачи, запрос в Яндекс, название отрасли ритейла (это
    ya.main_yandex(10, 'интернет-магазин одежды', 'Одежда') # название будет в названии страницы в результирующей таблице
    ya.main_yandex(10, 'интернет-магазин техники', 'Техника')
    ya.main_yandex(10, 'интернет-магазин детских товаров', 'Детские товары')
    ya.main_yandex(10, 'интернет-магазин техники', 'Техника')
    send_mail('YuraTheParser', 'yuradubi@gmail.com', 'Parsed data', 
              'Hi!', ['output.xlsx'], 'smtp.gmail.com', 
               587, 'taskshouldbedonebyalan@gmail.com', 'CRONis2weeks', True)


if __name__ == '__main__':
    print('Введите количество дней между запросами:')
    period = int(input())
    schedule.every(period).days.do(main)
    while True:
        schedule.run_pending()
        time.sleep(1) 