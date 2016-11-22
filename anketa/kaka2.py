import re
el = 'мама,папа'
res = re.search('(.+?),(.+)', el)
rr = res.group(1)
rrr = res.group(2)
print(rr)
print(rrr)
