import re
import json

from flask import Flask
from flask import url_for, render_template, request, redirect

def openfl(name1, name2):
    f = open(name1, 'r', encoding = 'UTF-8')
    fl = open(name2, 'r', encoding = 'UTF-8')
    s = f.readlines() + fl.readlines()
    f.close
    fl.close
#    print(s[10])
    return s

def makedc(s):
    dc = {}
    rss = []
    me = []
    es = []
    for el in s:
        res = re.search('lex: (.+?)\n', el)
        if res != None:
            key = res.group(1)
            es.append(key)
        m = re.search('gramm: (.+?)\n', el)
        if m != None:
            m = m.group(1)
            me.append(m)
        rs = re.search('trans_ru: (.+?)\n', el)
        if rs != None:
            rs = rs.group(1)
            rss.append(rs)
    zz = []
    for e in me:
        for l in rss:
            z = (e, l)
            zz.append(z)
    i = 0
    for el in es:
        dc[el] = zz[i]
        i += 1
    makejson(dc)
    otherdc(dc)
    return dc

def makejson(d):
    u = json.dumps(d, ensure_ascii = False)
    f = open('data.json', 'w', encoding = 'utf-8')
    f.write(u)
    f.close

def otherdc(dc):
    print(type(dc))
    udm = []
    dc2 = {}
    for key in dc:
        udm.append(key)
    for el in dc[key]:
        print(el)
    #makejson(dc2)
    
app = Flask(__name__)

@app.route('/')
def form(dc):
    if request.args:
        global udm
        udm = request.args['srch']
        if dc[udm]:
            global st
            st = dc[udm]
            return redirect(url_for('results'))
        else:
            return render_template('notfound.html')
    return render_template('form.html')

@app.route('/results')
def results():
    return render_template('result.html', x=udm, st=st)
    
if __name__ == '__main__':
    form(makedc(openfl('udm_lexemes_ADJ.txt', 'udm_lexemes_IMIT.txt')))
    app.run()
