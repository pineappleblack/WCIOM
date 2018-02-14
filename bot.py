from GenerateJSON import getJSON
import telebot
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging
import time

token = '436416709:AAH7sPnu-TeDUxF-JDlMm9OGrA5274AoIgo'

bot = telebot.TeleBot(token)

def send_message_to_channel():
    with open('testfile', 'w', encoding = 'UTF-8') as f:
        f.write(datetime.now().strftime("%A, %d. %B %Y %I:%M:%S") + '\n')
    
    with open('lastDate', encoding = 'UTF-8') as f:
        lastDate = f.read()
    
    url = 'https://wciom.ru/news/ratings/vybory_2018/'
    r = requests.get(url, verify = False)
    soup = BeautifulSoup(r.text, 'lxml')
    table = soup.findAll('table', {'id': 'tableprez'})[-1]
    date = table.tr('th')[-1].text
    
    if lastDate != date:
        bot.send_message('@wciomrbc', 'Обновление от '+date)
        getJSON()
        with open('lastDate', 'w', encoding = 'UTF-8') as f:
            f.write(date)
        f = open('wciom_candidates_2018.json')
        bot.send_document('@wciomrbc', f)
        f.close()
    time.sleep(1)
    return
	
if __name__ == '__main__':
    # Избавляемся от спама в логах от библиотеки requests
    logging.getLogger('requests').setLevel(logging.CRITICAL)
    # Настраиваем наш логгер
    logging.basicConfig(format='[%(asctime)s] %(filename)s:%(lineno)d %(levelname)s - %(message)s', level=logging.INFO,
                        filename='bot_log.log', datefmt='%d.%m.%Y %H:%M:%S')
    while True:
        send_message_to_channel()
        logging.info('[App] Script went to sleep.')
        time.sleep(5*60)

    logging.info('[App] Script exited.\n')