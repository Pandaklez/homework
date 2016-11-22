f = open('data.csv', 'r', encoding = 'utf-8')
ss = f.readlines()
f.close
#ss.remove('\n')
#for i in range(len(ss)):
#    ss.pop([i+1])
#for line in ss:
#    if line == '\n':
#print(ss)
k = []
for line in ss:
    line = line.strip('\n\r\t')
    if line != '':
        k.append(line)
#for line in ss:
#    line.strip('\n, \r')
        
print('\n'.join(k), end = '')
