import requests
inpute = input('alt food')
r = requests.post('http://127.0.0.1:8080/alternative',json={
    'food':inpute,
    'lowCarb':True,
    'glutenFree':False,
    'dairyFree':True
    })
print(r.json())
rjson = r.json()
alternative = rjson['alternative_food']

input()
r = requests.post('http://127.0.0.1:8080/near',json={'food':alternative})
print(r.text)