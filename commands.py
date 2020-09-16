# -*- coding: UTF-8 -*-

import telebot
import telebot.types as types
import csv
import string
import config

def msg_to_list(message):
    return message.text.lower().translate(str.maketrans('','',string.punctuation)).split(' ')

def addkeywords(message, stop_words=False):
    doc = 'keywords.csv' if not stop_words else 'stopwords.csv'
    keylist = message.text.lower().split(',')
    with open(doc, 'a', newline='', encoding='UTF-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(keylist)
    print('Keywords added')


def addadmins(message):
    doc = 'admins.csv'
    if message.contact:
        contacts = {str(message.contact.user_id)}
    elif message.text:
        contacts = set(message.text.lower().split(','))
    with open(doc, 'a', newline='', encoding='UTF-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(contacts)
    print('Admins added')
    
    
def showinfo():
    config.reload()
    return f'Ключевые слова: {config.KEYWORDS}\n\nСТОП-слова: {config.STOPWORDS}\n\nАдмины: {config.ADMINS}'
    
is_admin = lambda message: True if str(message.from_user.id) in config.ADMINS else False


def delkeywords(message):
    keylist = message.text.lower().split(',')
    newlist = config.KEYWORDS.difference(keylist)
    print(newlist)
    with open('keywords.csv', 'w', newline='', encoding='UTF-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(newlist)
        
def delstopwords(message):
    keylist = message.text.lower().split(',')
    newlist = config.STOPWORDS.difference(keylist)
    with open('stopwords.csv', 'w', newline='', encoding='UTF-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(newlist)

def deladmins(message):
    keylist = message.text.lower().split(',')
    newlist = config.ADMINS.difference(keylist)
    with open('admins.csv', 'w', newline='', encoding='UTF-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(newlist)