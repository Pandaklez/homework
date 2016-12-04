import urllib.request as ur
import re
import html
import os

def download():
    f = open('ull.txt', 'r', encoding = 'utf-8')
    s = f.read()
    f.close()
    arr = s.split(' ')
    k = []
    for el in arr:
        page = ur.urlopen(el)
        text = page.read().decode('UTF-8')
        clean_t = cleantext(text)
        k.append(clean_t)
    return k

def sts(k):
    d = {}
    i = 0
    for el in k:
        h = set()
        rr = el.split(' ')
        for word in rr:
            word = word.lower()
            word = word.strip(',.<>?/\'":;#№!~\n\t[]{}*+-_()1234567890=©\xa0«»')
            if word != '':
                h.add(word)
        i += 1
        d[i] = h
    return d

def intersect(d = {}):
    for key in d:
        if key == 1:
            set1 = d[key]
        elif key == 2:
            set2 = d[key]
        elif key == 3:
            set3 = d[key]
        else:
            set4 = d[key]
    cross = set1 & set3 & set4 & set2
    filewrite('cross.txt', cross)

    df1 = set1 - set2 - set3 - set4
    df2 = set2 - set1 - set3 - set4
    df3 = set3 - set1 - set2 - set4
    df4 = set4 - set1 - set2 - set3
    dif = list(df1) + list(df2) + list(df3) + list(df4)
    filewrite('dif.txt', dif)
    return dif

def filewrite(filename, var):
    f = open(filename, 'w', encoding = 'utf-8')
    f.close
    cr = sorted(list(var))
    if cr != []:
        for el in cr:
            f = open(filename, 'a', encoding = 'utf-8')
            f.write(str(el)+'\n')
    else:
        f.write('Пустое множество')
    f.close

def freq(dif, k):
    p = []
    for el in k:
        rr = el.split(' ')
        for word in rr:
            word = word.lower()
            word = word.strip(',.<>?/\'":;#№!~\n\t\r[]{}*+-_()1234567890=©\xa0«»')
            if word != '':
                p.append(word)
    dc = {}
    for el in dif:
        if el in p:
            fr = p.count(el)
            dc[el] = fr
    x = []
    for key in dc:
        fr = dc[key]
        if fr > 1:
            x.append(key)
    f = open('dif.txt', 'a', encoding = 'utf-8')
    f.write('======== Словоформы из симметрической разницы с частотностью > 1 ======== \n')
    for el in x:
        f.write(str(el)+'\n')
        f.close
        
def cleantext(text):
    html_content = '<html>....</html>'
    reg = re.search('js-mediator-article".*?>(.+?)<div (class="b-social|id="bl)', text, flags = re.DOTALL)
    if reg != None:
        clean_t = reg.group(1)
    else:
        reg = re.search('("content|bold mrgbtm20)">(.+?)(&#x37|<!-- tags)', text, flags = re.DOTALL)
        if reg != None:
            clean_t = reg.group(2)
    regScript = re.compile('script"?>.*?</script>', flags = re.DOTALL)
    regComment = re.compile('<!--.*?-->', flags = re.DOTALL)
    regTag = re.compile('<.*?>', flags = re.DOTALL)
    regAdvert = re.compile('Реклама.*', flags = re.DOTALL)

    clean_t = regScript.sub("", clean_t)
    clean_t = regComment.sub("", clean_t)
    clean_t = regTag.sub("", clean_t)
    clean_t = regAdvert.sub("", clean_t)
    clean_t = html.unescape(clean_t)
    return clean_t

def main():
    freq(intersect(sts(download())), download())

if __name__ == '__main__':
    main()
