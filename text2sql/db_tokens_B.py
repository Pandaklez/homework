import os
import re

from flask import Flask
from flask import url_for, render_template, request, redirect

def openfile():
    os.system('C:\\Annet\\mystem -nd C:\\Annet\\annak.txt C:\\Annet\\annak2.txt')
    f = open('C:\\Annet\\annak2.txt', 'r', encoding = 'UTF-8')
    s = f.readlines()
    f.close()
    j = []
    for line in s:
        mm = re.sub('{.*?}', '', line)
        j.append(mm)
#    print(j)
    return j

def makewords(s):
    s1 = []
    for line in s:
        words = line.split(' ')
        for word in words:
            word = word.lower()
            word = word.strip(' <>/\'#№~\n\t[],.;:!?"{}*+_-()1234567890=')
            if word != '':
                s1.append(word)
#    print(s1)
    return s1

def makelemmas(s1):
#    print(s1)
    os.system('C:\\Annet\\mystem -nd C:\\Annet\\annak.txt C:\\Annet\\annak_lemma.txt')
    f = open('C:\\Annet\\annak_lemma.txt', 'r', encoding = 'UTF-8')
    ms = f.read()
    f.close()
    tables(s1)
    res = lemmas(ms)
    zweitable(res, s1)
#    print(type(ms))
    return ms

def lemmas(ms):
    res = []
    rs = re.findall('(.*?){(.*?)}\n', ms)
    if rs != []:
        for el in rs:
            if el not in res:
                res.append(el)
    return res

def tables(s1):
#    f = open('C:\\Annet\\annak.txt', 'r', encoding = 'UTF-8')
#    nm = f.readlines()
#    f.close()
#    nam = nm[0]
#    nam = nam.strip('\n')
    f = open('DB.txt', 'w', encoding = 'UTF-8')
    f.write('CREATE TABLE `Words` (`id` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,`wordform` TEXT,`punc1` TEXT, `punc2` TEXT, `number_in_text` INTEGER UNIQUE, `id_table2` INTEGER);\n')
    f.write('CREATE TABLE `Analysis` (`id` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,`lemma` TEXT,`wordform` TEXT);\n')
    f.close()
    
def zweitable(res, s1):
#    f = open('C:\\Annet\\annak.txt', 'r', encoding = 'UTF-8')
#    nm = f.readlines()
#    f.close()
#    nam = nm[0]
#    nam = nam.strip('\n')
    lemma = []
    wordform = []
    d = {}
    for el in res:
        wr = str(el[0])
        wr2 = str(el[1])
        wr = wr.lower()
        wr2 = wr2.lower()
        wordform.append(wr)
        lemma.append(wr2)
        d[wr] = wr2
    lemmaset = set(lemma)
    lemma = list(lemmaset)
#    print(res)
    f = open('DB.txt', 'a', encoding = 'UTF-8')
    i = 1
    k = 0
    icx = []
    for el in s1:
        elle = d[el]
        k = lemma.index(elle) + 1
#        print(elle, str(k))
        punc2 = ''
        f.write('insert into Words (wordform, punc1, punc2, number_in_text, id_table2) values (\''\
                + el +'\', \'\',\'' + punc2 + '\','+ str(i) +','+ str(k) +');\n')
        if k not in icx:
            icx.append(k)
            f.write('insert into Analysis (id, wordform, lemma) values ('+ str(k) +',\'' + el + '\',\''+ elle +'\');\n')
        i += 1
    f.close()

app = Flask(__name__)

@app.route('/')
def form():
    if request.args:
        text = request.args[r'text']
#        nam = request.args['nam']
        f = open('C:\\Annet\\annak.txt', 'w', encoding = 'UTF-8')
        f.write(text)
#        f.write(nam + '\n' + text)
        f.close()
        main()
        return render_template('thanks.html', text=text) # , nam=nam)
    return render_template('form.html')

def main():
    makelemmas(makewords(openfile()))

if __name__ == '__main__':
    app.run(debug = True)
#    main()
