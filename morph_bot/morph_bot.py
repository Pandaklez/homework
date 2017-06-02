from pymystem3 import Mystem
from pymorphy2 import MorphAnalyzer
import numpy

import telebot
import flask
import conf
import phrases
#import shelve
import json
import csv
import random

f = open('w.txt', 'r', encoding = 'utf-8')
s = f.readlines()
f.close()
words = []
for el in s:
    word = el.strip('\n\t\r')
    words.append(word)

morph = MorphAnalyzer()

#with open('db.json', 'w', encoding='utf-8') as f2:
#    json.dump(d_inner, f2)

bot = telebot.TeleBot(conf.TOKEN)

@bot.message_handler(commands = ['start'])
def welcome(message):
    bot.send_message(message.chat.id, phrases.start)
@bot.message_handler(commands = ['help'])
def welcome(message):
    bot.send_message(message.chat.id, phrases.helpp)
    
@bot.message_handler(func = lambda m: True)
def len_message(message):
    mes = message.text.split(' ')
    ms = []
    for word in mes:
        word = word.strip(',.<>?/\'":;#№!~\n\t\r[]{}*+-_()1234567890=')
        #an = morph.parse(word)[0]
        length = len(mes)
        ms.append(word)
    d = tags(ms)
    dc = infl(d)
    lemas = inflect(dc, d)
    #ans = ' '.join(lemas)
    bot.send_message(message.chat.id, lemas)

def tags(ms):
    pos = []
    z = []
    anim = []
    aspect = []
    case = []
    gender = []
    involvement = []
    mood = []
    number = []
    person = []
    tense = []
    transitivity = []
    voice = []
    for el in ms:
        ana = morph.parse(el)[0]
        z.append(ana.normal_form)
        pos.append(ana.tag.POS)
        anim.append(ana.tag.animacy)
        aspect.append(ana.tag.aspect)
        gender.append(ana.tag.gender)
        involvement.append(ana.tag.involvement)
        mood.append(ana.tag.mood)
        number.append(ana.tag.number)
        person.append(ana.tag.person)
        tense.append(ana.tag.tense)
        transitivity.append(ana.tag.transitivity)
        voice.append(ana.tag.voice)
    init_lexeme = get_rows('lexeme')
    #rep = []
    #reply = ' '
    #for i in range(0, length):
    #    rep.append(init_lexeme[i])
    #repl = reply.join(rep)

    n = 0
    d = {}
    for word in z:
        d[word] = {}
        d[word]['id'] = n
        d[word]['pos'] = str(pos[n])
        d[word]['anim'] = anim[n]
        d[word]['aspect'] = aspect[n]
        d[word]['gender'] = gender[n]
        d[word]['involvement'] = involvement[n]
        d[word]['mood'] = mood[n]
        d[word]['number'] = number[n]
        d[word]['person'] = person[n]
        d[word]['tense'] = tense[n]
        d[word]['transitivity'] = transitivity[n]
        d[word]['voice'] = voice[n]
        n += 1
    with open('message_tags.json', 'w', encoding='utf-8') as f2:
        json.dump(d, f2, ensure_ascii = False)
    return d

def infl(d):
    with open("out.csv", 'r') as f: #В другой проге сделать этот файл большим
        dc = {}
        for line in f.readlines()[1:]:
            line = line.split(',')
            ld = line[1]
            lw = line[0]
            if ld not in dc:
                dc[ld] = []
            dc[ld].append(lw)
    with open('message_tags.json', 'a', encoding='utf-8') as f2:
        json.dump(dc, f2, ensure_ascii = False)
    stro = inflect(dc, d)
    return dc, stro

def inflect(dc, d):
    tag = ['number', 'anim', 'aspect', 'gender', 'involvement', 'mood',\
           'person', 'tense', 'transitivity', 'voice']
    lemas = {}
    wr = ''
    stroka = ''
    lis = []
    kulis = []
    for word in d:
        ps = d[word]['pos']
        n = int(d[word]['id'])
        with open('tmp.txt', 'w', encoding='utf-8') as f4:
            f4.write(str(dc[ps]))
        f4.close()
        with open('tmp.txt', 'r', encoding='utf-8') as f4:
            ls = f4.read()
            ls = ls.strip('[]')
            lis = ls.split(', ')
        for li in lis:
            li = li.strip('""')
            kulis.append(str(li))
        #lis = dc[ps] # СПисок слов одной и той же части речи ps
        #p = numpy.random.choice(lis, size=None, replace=True, p=None)
        #random.shuffle(lis) # Шаффлим этот список 
        p = random.choice(kulis) # рандомизатор
        wr = morph.parse(p)[0]
        rer = ''
        for t in tag:
            tags = {d[word][t]}
            try:
                wr.inflect(tags)
                rer = wr.word
            except ValueError or AttributeError:
                rer = wr.word
        lemas[n] = rer
        with open('message_tags.json', 'a', encoding='utf-8') as f2:
            json.dump(dc[ps], f2, ensure_ascii = False)
    for x in sorted(lemas.keys()):
        stroka += lemas[x] + ' '
    return stroka
          
def get_rows(var):
    s = csv.DictReader(open("out.csv"))
    cc = []
    for row in s:
        content = row[var]
        cc.append(content)
    return cc

if __name__ == '__main__':
    bot.polling(none_stop=True)
