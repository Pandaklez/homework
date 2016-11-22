import os
import json
tpath = os.getcwd()
n = []
lg = []
ass = []
ass1 = []
dd = {}
if os.path.isfile(tpath + '\\data.json'):
    f = open('data.json', 'r', encoding = 'utf-8')
    k = f.read()
    f.close
    dd = json.loads(k)
    for key in dd:
        n = dd["yourname"]
        lg = dd["language"]
        ass = list(dd["assess"])
        ass1 = list(dd["assess1"])
    name = 'hhhh'
    lang = 'jjjjj'
    assess = '1'
    assess1 = '5'
    n.append(name)
    lg.append(lang)
    ass.append(assess)
    ass1.append(assess1)
    print(ass)
    dic = {'yourname': n, 'language': lg, 'assess': assess, 'assess1': assess1}
    u = json.dumps(dic)
else:
    print("Питон бобо")
