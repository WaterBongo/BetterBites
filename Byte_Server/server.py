import flask
from flask import request
import openai,json,ast,requests,flask_cors
from flask_cors import CORS

config_json = open('config.json', 'r')
config = json.load(config_json)
openai.api_key = config['openai_key']
maps_api = config['maps_api']
config_json.close()



app = flask.Flask('nutrition')
CORS(app)
def find_food(food):
    msgs = []
    msgs.append({"role": "system", "content": """
please respond to my questions with the format 
please also dont say anything else but the responses

{'old_food' : [the food that we need to find the alternative for], 
'alternative_food' : [alternative food please dont use any punctionation],
'why' : [why is this a good alternative],
'nutrition_facts' : {
"old" : {
"calories" : 'calorie of food (please only put a number, not letters)',
"total_fat" : "total fat"(please only put a number, not letters),
},
"new" : "give the same format of nutiriion as the [food we need to find a alternative for]",

      }
}    
    """})
    msgs.append({"role": "user", "content": f"i want to find a alternative for {food}"})
    e =openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=msgs
)
    print(e['choices'][0]['message']['content'])
    return e['choices'][0]['message']['content']


def find_location_with_food(food_to_find,user_location):
    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
    params = {
        #please search in california
        'location': user_location,
        'query': food_to_find,
        'key': 'AIzaSyDximrySZEr37jflb65cjUg-AP41rLuhm8'
    }

    # Send a GET request to the API endpoint
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract the JSON data from the response
        data = response.json()

        # Check if any results were returned
        if len(data['results']) > 0:
            # Get the name and address of the first result
            name = data['results'][0]['name']
            address = data['results'][0]['formatted_address']

            # Print the name and address of the first result
            print(f"The first result is {name} at {address}")
            return (name,address)
        else:
            return (False,False)
    else:
        print("Request failed")

# def address_to_Long_Lat(address):
#     #use the google api to turn the address into a longituide and latituide
#     url = 'https://maps.googleapis.com/maps/api/geocode/json'
#     params = {
#         'address': address,
#         'key': 'AIzaSyDximrySZEr37jflb65cjUg-AP41rLuhm8'
#     }
#     response = requests.get

@app.route('/')
def index():
    return 'Hello world'




@app.route('/alternative',methods=['POST'])
def alternatives():
    #get food from the post json
    rjson = request.json
    food = rjson['food']
    lowcarb = rjson['lowCarb']
    glutenfree = rjson['glutenFree']
    dairyFree = rjson['dairyFree']
    #check if any of them are true if more then 2 are true then add them still
    if lowcarb == True:
        food = food + ' low carb'
    if glutenfree == True:
        food = food + ' gluten free'
    if dairyFree == True:
        food = food + ' dairy free'


    food_json = ast.literal_eval(find_food(food))
    #make the json look prettier
    food_json = json.dumps(food_json,indent=4)

    return food_json

@app.route('/near',methods=['POST'])
def near():
    food = request.json['food']
    user_location = request.json['location']
    if user_location == '':
        user_location = '34.0522,-118.2437'
    location = find_location_with_food(food,user_location)
    return {'place':location[0],'address':location[1]}
app.run('0.0.0.0',port=8080)