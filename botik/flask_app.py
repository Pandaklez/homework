import telebot
import conf
import flask

WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST,conf.WEBHOOK_PORT)

WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)

#conf.TOKEN #check if we can get token from file
bot = telebot.TeleBot(conf.TOKEN, threaded=False)
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

app = flask.Flask(__name__)

@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'It is working'

@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    #code generating bot's reply to the message
    bot.send_message(message.chat.id, 'Hi, bro ;)\n'
                     'I can count number of words in your message! Just write something:)')

@bot.message_handler(func=lambda m: True)
def len_message(message):
    m = message.text
    arr = m.split(' ')
    bot.send_message(message.chat.id, 'In your message {} words'.format(len(arr)))

# обрабатываем вызовы вебхука = функция, которая запускается, когда к нам постучался телеграм 
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)
        
#go to python anywhere. go to bash
#we should install modules in bash

