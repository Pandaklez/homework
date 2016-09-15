import urllib.request as ur
import sys
import re
import os

def download():
    page = ur.urlopen('http://ngisnrj.ru/')
    text = page.read().decode('UTF-8')
    return(text)

def findarticles(text):
    m = re.findall('data-url-args-store>(.+?)<', text)
    if m != None and m != []:
        return m

def artcls(m):
    arr = []
    mm = str(m).split(' ')
    for el in mm:
        el = el.strip('[],')
        if el != '':
            arr.append(el)
    articles = ' '.join(arr)
    return articles

def makingfile(articles):
    newpath = r'E:\\Anna\\Desktop\\Newspaper_Наша_жизнь'
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    try:
        filename = 'E:\\Anna\\Desktop\\Newspaper_Наша_жизнь\\articlenames.txt'
        file = open(filename, 'w')
        file.write(articles)
        file.close()
    except:
        print('Error with making path and txt file occured')
        sys.exit(0)
    
def main():
    makingfile(artcls(findarticles(download())))

if __name__ == '__main__':
    main() 
