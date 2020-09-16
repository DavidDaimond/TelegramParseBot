# -*- coding: UTF-8 -*-

import csv
import cherrypy


TOKEN = ''

DESCRIPTION = 'Список команд с кратким описанием их функций:\n\n/showinfo - показывает информацию о ключевых словах, СТОП-словах и админах\n\n/addkeywords - добавить ключевые слова через запятую (БЕЗ ПРОБЕЛОВ!)\n\n/delkeywords - удалить ключевые слова\n\n/addstopwords - добавить СТОП-слова\n\n/delstopwords - удалить СТОП-слова\n\n/addadmins - добавить админов. Принимает как список из ID, так и сообщения в виде контакта\n\n/deladmins - удалить админов по их ID'

WEBHOOK_HOST = ''
WEBHOOK_PORT = 443
WEBHOOK_LISTEN = '0.0.0.0'

WEBHOOK_SSL_CERT = './webhook_cert.pem'
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'

WEBHOOK_URL_BASE = f"https://{WEBHOOK_HOST}:{WEBHOOK_PORT}"
WEBHOOK_URL_PATH = f'/{TOKEN}/'

class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("UTF-8")
            update = telebot.types.Update.de_json(json_string)

            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)


with open('keywords.csv', newline='', encoding='UTF-8') as keywords:
    data = csv.reader(keywords, delimiter=';')
    KEYWORDS = set()
    for row in data:
        KEYWORDS.update(set(row))
    print(f'KEYWORDS: {KEYWORDS}')

with open('stopwords.csv', newline='', encoding='UTF-8') as stopwords:
    data = csv.reader(stopwords, delimiter=';')
    STOPWORDS = set()
    for row in data:
        STOPWORDS.update(set(row))
    print(f'STOPWORDS: {STOPWORDS}\n')

with open('admins.csv', newline='', encoding='UTF-8') as admins:
    data = csv.reader(admins, delimiter=';')
    ADMINS = set()
    for row in data:
        ADMINS.update(set(row))
    print(f'ADMINS: {ADMINS}\n')

#Commands to update dbases 

def reload():
    global KEYWORDS
    global STOPWORDS
    global ADMINS
    
    with open('keywords.csv', newline='', encoding='UTF-8') as keywords:
        data = csv.reader(keywords, delimiter=';')
        KEYWORDS = set()
        for row in data:
            KEYWORDS.update(set(row))

    
    with open('stopwords.csv', newline='', encoding='UTF-8') as stopwords:
        data = csv.reader(stopwords, delimiter=';')
        STOPWORDS = set()
        for row in data:
            STOPWORDS.update(set(row))
    
        
    with open('admins.csv', newline='', encoding='UTF-8') as admins:
        data = csv.reader(admins, delimiter=';')
        ADMINS = set()
        for row in data:
            ADMINS.update(set(row))
    print(f'All params was updated')