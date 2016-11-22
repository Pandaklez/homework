import csv
import re
f = open('data.csv', 'r', encoding = 'utf-8')
s = f.readlines()
f.close
print(s)
for line in s:
    if line != '\n':
        print(line, end = '')
        res = re.search('(.+?),(.+?),(.+?),(.+?),(.+)', line)
        nm = res.group(1)
        lng = res.group(2)
        mo = res.group(3)
        fat = res.group(4)
        sn = res.group(5)
        print(nm)
        print(lng)
        print(mo)
        print(fat)
        print(sn)
