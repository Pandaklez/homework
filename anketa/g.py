import json
import re
import csv
import os.path

from flask import Flask
from flask import url_for, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def form():
    urls = {'Анкета (эта страница)': url_for('form'),
            'Страница с json': url_for('jjson'),
            'Статистика': url_for('stats'),
            'Поиск': url_for('srch')}
    if request.args:
        name = request.args['name']
        lang = request.args['lang']
        fath = request.args['father']
        mum = request.args['mother']
        sun = request.args['sun']
        if name != "" and lang != "" and fath != "" and mum != "" and sun != "":
            with open('data.csv','a', encoding = 'utf-8') as inFile:
                writer = csv.DictWriter(inFile, fieldnames=("name", "language", "mother", "father", "sun"))
                writer.writerow({'name': name, 'language': lang, 'mother': mum, 'father': fath, 'sun': sun})
                inFile.close()
        tpath = os.getcwd()
        n = []
        lg = []
        m = []
        fa = []
        su = []
        dd = {}
        if os.path.isfile(tpath + '\\data.json'):
            f = open('data.json', 'r', encoding = 'utf-8')
            k = f.read()
            f.close
            dd = json.loads(k)
            for key in dd:
                n = dd["yourname"]
                lg = dd["language"]
                m = dd["mother"]
                fa = dd["father"]
                su = dd["sun"]
            if name != "" and lang != "" and fath != "" and mum != "" and sun != "":
                n.append(name)
                lg.append(lang)
                m.append(mum)
                fa.append(fath)
                su.append(sun)
                dic = {'yourname': n, 'language': lg, 'mother': m, 'father': fa, 'sun': su}
                u = json.dumps(dic, ensure_ascii = False)
                f = open('data.json', 'w', encoding = 'utf-8')
                f.write(u)
                f.close
        else:
            if name != "" and lang != "" and fath != "" and mum != "" and sun != "":
                n.append(name)
                lg.append(lang)
                m.append(mum)
                fa.append(fath)
                su.append(sun)
                dic = {'yourname': n, 'language': lg, 'mother': m, 'father': fa, 'sun': su}
                dd = json.dumps(dic, ensure_ascii = False)
                f = open('data.json', 'w', encoding = 'utf-8')
                f.write(dd)
                f.close  
        return render_template('thanks.html', name=name, sun=sun, mother=mum, father=fath, lang=lang)
    return render_template('form.html', urls=urls)

@app.route('/json')
def jjson():
    f = open('data.json', 'r', encoding = 'utf-8')
    s = f.read()
    f.close
    return render_template('jjson.html', s=s)

@app.route('/search')
def srch():
    f = open('data.csv', 'r', encoding = 'utf-8')
    ss = f.readlines()
    f.close
    k = []
    for line in ss:
        line = line.strip('\n\r\t')
        if line != '':
            k.append(line)
    dc = {}
    i = 0 
    for el in k:
        if i != 0:
            res = re.search('(.+?),(.+?),(.+?),(.+?),(.+)', el)
            if res != None:
                nm = res.group(1)
                lng = res.group(2)
                mo = res.group(3)
                fat = res.group(4)
                sn = res.group(5)
                dc[lng] = [mo, fat, sn]
        i += 1
    if request.args:
        global srch
        srch = request.args['srch']
        if dc[srch]:
            global strg
            strg = ', '.join(dc[srch])
            return redirect(url_for('results'))
        else:
            return render_template('notfound.html', x=srch)
    return render_template('srch.html', dc=dc, lng=lng, mo=mo, fat=fat, sn=sn)

@app.route('/results')
def results():
    return render_template('result.html', x=srch, strg=strg)

@app.route('/stats')
def stats():
    csvFile = open('data.csv', 'r', encoding = 'utf-8')
    csvReader = csv.reader(csvFile)
    csvData = list(csvReader)
    with open('templates/stats1.html', 'w', encoding = 'utf-8') as html:
        html.write('''{% extends "base.html" %}
{% block content %}''')
        html.write('<p><h2>Статистика</h2></p>')
        html.write('''<!-- Latest compiled and minified CSS -->

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-table/1.8.1/bootstrap-table.min.css">

<!-- Latest compiled and minified CSS -->

<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css"> ''')
        html.write('<table data-toggle = "table" data-pagination = "true">\r')
        pp = ['Имя', 'Язык', 'Mother', 'Father', 'Sun']
        for col in pp:
            html.write('\t\t\t<th data-sortable="true">' + col + '</th>\r')
        html.write('\t\t</tr>\r\t</thead>\r')
        html.write('\t<tbody>\r')
        for row in csvData:
            html.write('\t\t<tr>\r')
            for col in row:
                html.write('\t\t\t<td>' + col + '</td>\r')
            html.write('\t\t</tr>\r')
        html.write('\t</tbody>\r')
        html.write('</table>\r')
        html.write('''
<!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.0/jquery.min.js"></script>

<!-- Latest compiled and minified JavaScript -->
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>

<!-- Latest compiled and minified JavaScript -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-table/1.8.1/bootstrap-table.min.js"></script>
''')
        html.write('{% endblock %}')
        html.close()
    return render_template('stats1.html')

if __name__ == '__main__':
   app.run()
