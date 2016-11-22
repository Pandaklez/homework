import pandas
import csv
import re
f = open('data.csv', 'r', encoding = 'utf-8')
s = f.readlines()
f.close
for line in s:
    if line != '\n':
        print(line, end = '')
        res = re.search('(.+?),(.+?),(.+?),(.+?),(.+)', line)
        nm = res.group(1)
        lng = res.group(2)
        mo = res.group(3)
        fat = res.group(4)
        sn = res.group(5)
        rw = [nm, lng, mo, fat, sn]
        f = pandas.read_csv("data.csv")
        tbl = pandas.DataFrame(rw, columns = ["Имя", "Язык", "mother", "father", "sun"])
