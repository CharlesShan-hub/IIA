import json

a = [11,12,13]
a.append(1)
prices = {
    'ACME': 45.23,
    'AAPL': 612.78,
    'IBM': a,
    'HPQ': 37.20,
    'FB': 10.75
}
 
#with open('price.json', 'w') as f:
#    json.dump(prices,f)

path = 'price.json'
with open(path, 'w', encoding='utf-8') as f:
	f.write(json.dumps(prices, indent=4, ensure_ascii=False))