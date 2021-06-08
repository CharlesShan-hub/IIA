import json
with open('price.json', 'r') as f:
    a = json.load(f)    #此时a是一个字典对象

 
print(a['IBM'])
'''
Out[47]: 45.23
'''