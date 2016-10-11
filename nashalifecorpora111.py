import os
import urllib.request as ur
import time
import re
import html
import sys

def gethtml(adrs, number, i):
    try:
        page = ur.urlopen(adrs)
        text = page.read().decode('UTF-8')
        print('PAGE EXISTS')
        
    except:
        print('No such page=' + str(number))
        text = ''
        return text

    clean_t = cleantext(text)
    z = 'issue__date\">.*?\..*?\.(.*?)\s'
    directory = '\\plain\\' + regularex(z, text)
    dr = regularex(z, text)
    catalog(directory)
    
    z = 'author__name\">(.*?)<'
    x1 = regularex(z, text)
    z = 'detail__title">.*?>(.*?)<'
    x2 = regularex(z, text)
    z = 'issue__date\">(.*?)\s'
    x3 = regularex(z, text)
    z = 'category=.+?\">(.*?)<'
    x4 = regularex(z, text)
    
    xx = "@au " + x1 + "\n" + "@ti " + x2 + "\n" + "@da " + x3 +\
             "\n" + '@topic ' + x4 + '\n' + '@url ' + adrs + "\n" + clean_t
    name = 'C:\\Annet\\news' + directory + '\\article' + str(number) + '.txt'
    writein(name, xx)
    if i == 1:       
        nm = 'path\tauthor\tsex\tbirthday\theader\tcreated\tsphere\tgenre_fi\ttype\ttopic\tchronotop\tstyle\taudience_age\taudience_level\taudience_size\tsource\tpublication\tpublisher\tpubl_year\tmedium\tcountry\tregion\tlanguage\n'
        writein('C:\\Annet\\news\\metadata.csv', nm)
    
    md = '%s\t%s\t\t\t%s\t%s\tпублицистика\t\t\t%s\t\tнейтральный\tн-возраст\tн-уровень\tрайонная\t%s\tНаша жизнь\t\t%s\tгазета\tРоссия\tБелгородская область\tru\n'
    mst = md % ('C:\\Annet\\news\\plain\\' + directory + '\\article' + str(number) + '.txt', x1, x2, x3, x4, adrs, dr) #dr это какая-то фигня
    writein('C:\\Annet\\news\\metadata.csv', mst)

    return text

        
def writein(name, xx):
    f = open(name, 'a', encoding = 'UTF-8')
    f.write(xx)
    f.close()



def regularex(z, text):
    reg = re.search(z, text, flags = re.DOTALL)
    if reg != None:
        m = reg.group(1)
        return m
    else:
        return ''


def cleantext(text):
    html_content = '<html>....</html>'
    clean_t = regularex('b-block-text__text\">(.*?)</div>', text)
    regScript = re.compile('<script>.*?</script>', flags = re.DOTALL) # все скрипты
    regComment = re.compile('<!--.*?-->', flags = re.DOTALL)  # все комментарии
    regTag = re.compile('<.*?>', flags = re.DOTALL)  # это рег. выражение находит все тэги
    regAdvert = re.compile('Реклама.*', flags = re.DOTALL)

    clean_t = regScript.sub("", clean_t)
    clean_t = regComment.sub("", clean_t)
    clean_t = regTag.sub("", clean_t)
    clean_t = regAdvert.sub("", clean_t)
    clean_t = html.unescape(clean_t)
    filename = 'C:\\Annet\\g.txt'
    f = open(filename, 'w', encoding = 'utf-8')
    f.write(clean_t)
    return clean_t


def catalog(directory):
    if not os.path.exists('C:\\Annet\\news' + directory):
        os.makedirs('C:\\Annet\\news' + directory)


def cat():
    directory = 'C:\\Annet\\news'
    dr1 = 'C:\\Annet\\news\\plain'
    dr2 = 'C:\\Annet\\news\\mystem-xml'
    dr3 = 'C:\\Annet\\news\\mystem-plain'
    if not os.path.exists(directory):
        os.makedirs(directory)
    if not os.path.exists(dr1):
        os.makedirs(dr1)
    if not os.path.exists(dr2):
        os.makedirs(dr2)
    if not os.path.exists(dr3):
        os.makedirs(dr3)

def labeledtxt(adrs, number, text):
    z = 'issue__date\">.*?\..*?\.(.*?)\s'
    directory = regularex(z, text)
#    print(type(directory))
        
    os.system('C:\\Annet\\mystem -ind C:\\Annet\\g.txt C:\\Annet\\h.txt')
    f = open('C:\\Annet\\h.txt', 'r', encoding = 'UTF-8')
    s = f.read()
    f.close()
    if not os.path.exists('C:\\Annet\\news\\mystem-plain\\' + directory):
        os.makedirs('C:\\Annet\\news\\mystem-plain\\' + directory)
    os.rename('C:\\Annet\\h.txt', 'C:\\Annet\\news\\mystem-plain\\' +\
              directory + '\\articlemsp' + str(number) +
              '.txt')
    
    os.system('C:\\Annet\\mystem -ind --format xml C:\\Annet\\g.txt C:\\Annet\\h.xml')
    f = open('C:\\Annet\\h.xml', 'r', encoding = 'UTF-8')
    s = f.read()
    f.close()
    if not os.path.exists('C:\\Annet\\news\\mystem-xml\\' + directory):
        os.makedirs('C:\\Annet\\news\\mystem-xml\\' + directory)
    os.rename('C:\\Annet\\h.xml', 'C:\\Annet\\news\\mystem-xml\\' +\
             directory + '\\articlexml' + str(number) + '.xml')

def main():
#вставить в цикле time.sleep() между скачиванием страниц
#здесь будет лежать цикл, перебирающий страницы
    adr = 'http://ngisnrj.ru/news/'
    i   = 0
    for number in range(236, 124735): #надо увеличить потом range
        adrs = adr + str(number) + '/'
        cat()
        i += 1
        text = gethtml(adrs, number, i)
#        print(text)
        if text == '':
            continue
        labeledtxt(adrs, number, text)
        time.sleep(2)

if __name__ == '__main__':
    main() 
