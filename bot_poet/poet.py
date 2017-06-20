import telebot
import flask
from flask import render_template
#import conf
import phrases
import urllib.request as ur
import urllib.parse as pars
import re
import html
from telebot import util
from pymorphy2 import MorphAnalyzer
import os

TOKEN = os.environ["TOKEN"]

bot = telebot.TeleBot(TOKEN, threaded=False)

bot.remove_webhook()
bot.set_webhook(url="https://hidden-plains-61544.herokuapp.com/bot")

#add webhooks

app = flask.Flask(__name__)

@app.route('/', methods=['GET', 'HEAD'])
def index():
    return render_template('index.html')

@bot.message_handler(commands = ['start'])
def welcome(message):
    bot.send_message(message.chat.id, phrases.start)
@bot.message_handler(commands = ['help'])
def welcome1(message):
    bot.send_message(message.chat.id, phrases.helpp)

@bot.message_handler(content_types=['text'])
def key_word(message):
    kw = message.text
    text = make_request(kw)
    if len(text) >= 4000:
        splitted_text = util.split_string(text, 3000)
        for repl in splitted_text:
            bot.send_message(message.chat.id, repl)
    else:
        bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['audio', 'sticker', 'document', 'video', 'voice', 'photo'])
def cant(message):
    bot.send_message(message.chat.id, phrases.cant)
    
def make_request(kw):
    kw = kw.lower()
    kw = kw.strip(',.<>?/\'":;#№!~\n\t[]{}*+-_()1234567890=')
    morph = MorphAnalyzer()
    kw_norm = morph.parse(kw)[0].normal_form
    key_word = pars.quote(kw_norm)
    req_url = "http://search2.ruscorpora.ru/search.xml?sort=gr_created&out=normal&dpp=10&spd=10&env=alpha&mycorp=&mysent=&mysize=&mysentsize=&mydocsize=&text=lexgramm&mode=poetic&ext=10&nodia=1&parent1=0&level1=0&lex1="\
              + str(key_word) + "&gramm1=&flags1=&sem1=&expand=full"
    f_html = ur.urlopen(req_url)
    text = f_html.read().decode('cp1251')
    clean_text = cleantext(text, kw)
    #with open('html.txt', 'w', encoding='cp1251') as f:
    #    f.write(text)
    #f.close()
    return clean_text

def cleantext(text, kw):
    m = re.search(r'<ul><li>(.*?)<span class="doc">', text, flags = re.DOTALL)
    if m != None:
        tet = m.group(1)
        regSpan1 = re.compile('</span>', flags = re.DOTALL)
        regSpan3 = re.compile('<span.*?>', flags = re.DOTALL)
        regSup = re.compile('<sup>.*?</sup>', flags = re.DOTALL)

        clean_t = regSpan1.sub("", tet)
        clean_t = regSpan3.sub("", clean_t)
        clean_t = regSup.sub("", clean_t)
        clean_t = re.sub('<br>', '\n', clean_t)
        clean_t = re.sub('<i>', '**', clean_t)
        clean_t = re.sub('</i>', '**', clean_t)
        clean_t = html.unescape(clean_t)
        clean_t = highlight(clean_t, kw)
        out = clean_t
    else:
        out = phrases.not_found
    return out

def highlight(clean_t, kw):
    morph = MorphAnalyzer()
    kw_lemm = morph.parse(kw)[0]
    kw_forms = kw_lemm.lexeme
    forms = []
    for el in kw_forms:
        forms.append(el.word)
    for form in forms:
        text = re.sub(form, form.upper(), clean_t)
        text = re.sub(form.capitalize(), form.upper(), text)
        clean_t = text
    return text

@app.route("/bot", methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)

if __name__ == '__main__':
    import os
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
