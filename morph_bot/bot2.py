from pymorphy2 import MorphAnalyzer

import telebot
import flask
import conf
import phrases
import json
import csv
import random
import re

bot = telebot.TeleBot(conf.TOKEN)

WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

app = flask.Flask(__name__)

#f = open('w.txt', 'r', encoding = 'utf-8')
#s = f.readlines()
#f.close()
#words = []
#for el in s:
#    word = el.strip('\n\t\r')
#    words.append(word)

morph = MorphAnalyzer()

#with open('db.json', 'w', encoding='utf-8') as f2:
#    json.dump(d_inner, f2)

@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'

@bot.message_handler(commands = ['start'])
def welcome(message):
    bot.send_message(message.chat.id, phrases.start)
@bot.message_handler(commands = ['help'])
def welcome1(message):
    bot.send_message(message.chat.id, phrases.helpp)
    
@bot.message_handler(func = lambda m: True)
def len_message(message):
    mes = message.text.split(' ')
    ms = []
    for word in mes:
        word = word.strip(',.<>?/\'":;#№!~\n\t\r[]{}*+-_()1234567890=')
        ms.append(word)

    d_us = take_changable(ms)
    dc = lexemes()
    decoder = gram()
    dus = decode_mess(d_us, decoder)
    lemas = select_words(dus, dc)
    reply = inflect(lemas, dus)
    
    bot.send_message(message.chat.id, reply)

def take_changable(ms):
    d_us = {}
    n = 0
    for el in ms:
        stol = morph.parse(el)
        tags = stol[0].tag.cyr_repr
        m = re.search('\s(\S*)', tags)
        if m != None:
            tg = m.group(1)
            tg = tg.split(',')
        else:
            tg = []
        m = re.search('([А-Я]*)', tags)
        pos = m.group(0)
        d_us[n] = {'tags' : tg, 'POS' : pos}
        n += 1
    with open('usery.json', 'w', encoding='utf-8') as f2:
        json.dump(d_us, f2, ensure_ascii = False)
    return d_us

def lexemes():
    with open("out.csv", 'r') as f: #В другой проге сделать этот файл большим
        dc = {}
        for line in f.readlines()[1:]:
            line = line.split(',')
            ld = line[1]
            lw = line[0]
            if ld not in dc:
                dc[ld] = []
            dc[ld].append(lw)
    with open('lexemes.json', 'w', encoding='utf-8') as f2:
        json.dump(dc, f2, ensure_ascii = False)
    return dc

def gram():
    with open("grammemes.csv", 'r') as f:
        decoder = {}
        for line in f.readlines()[1:]:
            line = line.split(';')
            key = line[1].strip('\n')
            value = line[0]
            decoder[key] = value
    with open('lexemes.json', 'a', encoding='utf-8') as f2:
        json.dump(decoder, f2, ensure_ascii = False)
    return decoder

def decode_mess(d_us, decoder):
    for key in d_us:
        pos = d_us[key]["POS"]
        if pos in decoder:
            d_us[key]["POS"] = decoder[pos]
        i = 0
        arr = list(d_us[key]["tags"])
        arr2 = []
        for el in arr:
            if el in decoder:
                arr2.insert(i, decoder[el])
            else:
                arr2.insert(i, "###")
            i += 1
        d_us[key]["tags"] = arr2
    with open('usery.json', 'a', encoding='utf-8') as f2:
        json.dump(d_us, f2, ensure_ascii = False)
    return d_us

def select_words(dus, dc):
    lemas = []
    for key in dus:
        pos = dus[key]["POS"]
        if pos in dc:
            lem = random.choice(dc[pos])
            lemas.append(lem)
    with open('usery.json', 'a', encoding='utf-8') as f2:
        json.dump(lemas, f2, ensure_ascii = False)
    return lemas

def inflect(lemas, dus):
    n = 0
    rep = []
    for word in lemas:
        m = morph.parse(word)[0]
        if n in dus:
            tags = dus[n]["tags"]
        for el in tags:
            m.inflect({el})
        n += 1
        rep.append(m.word)
    reply = ' '.join(rep)
    return reply

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)
        
#if __name__ == '__main__':
#    bot.polling(none_stop=True)
