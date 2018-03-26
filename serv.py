from flask import Flask, jsonify
import urllib3
import scrape
import train_light

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/app/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks' : tasks})

@app.route('/app/api/v1.0/tasks', methods=['POST'])
def evaluate():
    data = scrape.getName('realDonaldTrump')
    data['bot']= train_light.evaluate(data)
    return jsonify({'data' : data})



def response(botdata):
    http = urllib3.PoolManager()
    DOMAIN= 'http://127.0.0.1:5000'
    r = http.request('POST',DOMAIN,botdata)



if __name__ =='__main__':
    app.run(debug=True)