# -*- coding: UTF-8 -*-

import telebot
import telebot.types as types
import config
import commands
import random
import csv
import time
import cherrypy

bot = telebot.TeleBot(config.TOKEN)

last_message = ''

cherrypy.config.update({
    'server.socket_host': config.WEBHOOK_LISTEN,
    'server.socket_port': config.WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': config.WEBHOOK_SSL_CERT,
    'server.ssl_private_key': config.WEBHOOK_SSL_PRIV
})




@bot.message_handler(func=commands.is_admin, commands=['addadmins'])
def addadmins(message):
    global last_message
    last_message = 'addadmins'
    bot.send_message(message.chat.id, f'{message.from_user.first_name}, отправьте данные в виде контакта или списка из ID')


@bot.message_handler(func=lambda message: True if last_message == 'addadmins' else False, content_types=['text', 'contact'])
def addadmin(message):
    global last_message
    last_message = ''
    commands.addadmins(message)
    bot.send_message(message.chat.id, f'Новый админ добавлен!')    
    
@bot.message_handler(func=commands.is_admin, commands=['addkeywords'])
def addkeywords(message):
    global last_message
    last_message = 'addkeywords'
    bot.send_message(message.chat.id, f'{message.from_user.first_name}, напишите через запятую нужные слова, они будут добавлены в список ключевых слов')

@bot.message_handler(func=lambda message: True if last_message == 'addkeywords' else False, content_types=['text'])
def addkeyword(message):
    global last_message
    last_message = ''
    commands.addkeywords(message)
    config.reload()
    bot.send_message(message.chat.id, f'Добавлены ключевые слова: {message.text.split(",")}')


@bot.message_handler(func=commands.is_admin, commands=['addstopwords'])
def addstopwords(message):
    global last_message
    last_message = 'addstopwords'
    bot.send_message(message.chat.id, f'{message.from_user.first_name}, напишите через запятую нужные слова, они будут добавлены в список СТОП-слов')

@bot.message_handler(func=lambda message: True if last_message == 'addstopwords' else False, content_types=['text'])
def addstopword(message):
    global last_message
    last_message = ''
    commands.addkeywords(message, True)
    config.reload()
    bot.send_message(message.chat.id, f'Добавлены СТОП-слова: {message.text.split(",")}')

@bot.message_handler(func=commands.is_admin, commands=['delkeywords'])
def delkeywords(message):
    global last_message
    last_message = 'delkeywords'    
    bot.send_message(message.chat.id, f'{message.from_user.first_name}, напишите через запятую нужные слова, они будут удалены из списка ключевых слов')

@bot.message_handler(func=lambda message: True if last_message == 'delkeywords' else False, content_types=['text'])
def delkeyword(message):
    global last_message
    last_message = ''
    commands.delkeywords(message)
    config.reload()
    bot.send_message(message.chat.id, 'Указанные слова удалены')
    bot.send_message(message.chat.id, f'Текущее состояние базы данных: {commands.showinfo()}')


@bot.message_handler(func=commands.is_admin, commands=['delstopwords'])
def delkeywords(message):
    global last_message
    last_message = 'delstopwords'    
    bot.send_message(message.chat.id, f'{message.from_user.first_name}, напишите через запятую нужные слова, они будут удалены из списка СТОП-слов')

@bot.message_handler(func=lambda message: True if last_message == 'delstopwords' else False, content_types=['text'])
def delkeyword(message):
    global last_message
    last_message = ''
    commands.delstopwords(message)
    config.reload()
    bot.send_message(message.chat.id, 'Указанные слова удалены')
    bot.send_message(message.chat.id, f'Текущее состояние базы данных: {commands.showinfo()}')


@bot.message_handler(func=commands.is_admin, commands=['deladmins'])
def delkeywords(message):
    global last_message
    last_message = 'deladmins'    
    bot.send_message(message.chat.id, f'{message.from_user.first_name}, напишите через запятую ID админов, они будут удалены из списка админов')

@bot.message_handler(func=lambda message: True if last_message == 'deladmins' else False, content_types=['text'])
def delkeyword(message):
    global last_message
    last_message = ''
    commands.deladmins(message)
    config.reload()
    bot.send_message(message.chat.id, 'Указанные админы удалены')
    bot.send_message(message.chat.id, f'Текущее состояние базы данных: {commands.showinfo()}')


@bot.message_handler(func=commands.is_admin, commands=['showinfo'])
def showinfo(message):
    bot.send_message(message.chat.id, commands.showinfo())

@bot.message_handler(func=commands.is_admin, commands=['info'])
def info(message):
    bot.send_message(message.chat.id, config.DESCRIPTION)

@bot.message_handler(func=commands.is_admin, commands=['chats'])
def chats(message):
    bot.send_message(message.chat.id, bot.get_me())

@bot.message_handler()
def bot_added(message):
    if bot.get_me['id'] in message.new_chat_members:
        for admin in config.ADMINS:
            bot.send_message(admin, f'I had been added to group')

@bot.message_handler(commands=['start', 'main'])
def start_command(message):
    #if message.from.id == :
    bot.send_message(message.chat.id, f'{message.from_user.id} - your_id, mr. {message.from_user.last_name}')
    print(message.from_user.username, 'написал боту')


#
@bot.message_handler(content_types=['text'])
def send_admin(message):
    if (config.KEYWORDS & set(commands.msg_to_list(message))) and not (config.STOPWORDS & set(commands.msg_to_list(message))):
        for admin in ADMINS
            bot.send_message(int(admin), f'Пользователь {message.from_user.username} написал: \n/{message.text}/ \nВ чате: {message.chat.title}.')
            bot.forward_message(int(admin), message.chat.id, message.message_id)
            print(message.from_user.username, 
            f'написал боту\nНайдено ключевых слов: {len(config.KEYWORDS & set(commands.msg_to_list(message)))}\nНайдено стоп слов: {len((config.STOPWORDS & set(commands.msg_to_list(message))))}')


"""
def botwork():
    try:
        print('BOT STARTED HIS WORK!')
        print(bot.get_webhook_info())
        bot.remove_webhook()
        bot.polling(none_stop=True)
    except Exception as ex:
        bot.send_message(649697634, f'Bot disabled his work with {ex}. Reboot....')
        print(f'Bot disabled his work with {ex}. Reboot....')
        time.sleep(10)
        bot.stop_bot()
        bot.stop_polling()
        botwork()
"""

def botwork():
    try:
        bot.remove_webhook()
        bot.set_webhook(url=config.WEBHOOK_URL_BASE + config.WEBHOOK_URL_PATH, certificate=open(config.WEBHOOK_SSL_CERT, 'r'))
        cherrypy.quickstart(config.WebhookServer(), config.WEBHOOK_URL_PATH, {'/': {}})
        print('BOT STARTED HIS WORK!')
        print(bot.get_webhook_info())
    except Exception as ex:
        bot.send_message(649697634, f'Bot disabled his work with {ex}. Reboot....')
        time.sleep(10)
        botwork()


if __name__ == '__main__':
    botwork()