from flask import Flask,jsonify
import take_in_data
import scrape
import Mongo2
import Keras
import pandas

app = Flask(__name__)
model = Keras.train_model(Keras.create_baseline())

##Evaluate is used on newly scraped data
def evaluate(data):

    print(data)
    data = {
        "favourites": 0,
        "followers": 50006160,
        "following": 45,
        "moments": 6,
        "tweets": 37245,
        "verified": 1
    }
    print(data)
    data = pandas.DataFrame(data, index=[6])
    data = data.values
    prediction, probability = model.predict_classes(data), model.predict(data)
    probability = probability * 100
    print(prediction)
    print(probability)
    return prediction,probability

@app.route('/<string:name>')
def evaluateName(name):
    ##First query the db
    x = Mongo2.queryUname(name)
    ##If db returns nothing
    if x is not None:
        data = scrape.getName(name)
        if data is None:
            data = {'name':'Does not exist'}
            return jsonify(data)
        data.pop('name')
        image = data.pop('image')
        botvalue,probability = evaluate(data)
        data['bot'],data['probability'],data['name'],data['image'] = botvalue, probability, name,image
        Mongo2.insertOrUpdate(data)
        data.pop('_id')
    else:
        data = x

    return jsonify(data)

app.run(debug=True)