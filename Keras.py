import numpy
import pandas
from flask import jsonify
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold

import Mongo2
import scrape

train_path = 'train.csv'  # ~\Documents\SEC203DAT\Train1
test_path = 'test.csv'  # ~\Documents\SEC203DATTest1


def getData():
    # train data
    dataframe = pandas.read_csv(train_path)
    dataframe.pop('name')
    dataset = dataframe.values
    train_x = dataset[:, 1:7]
    train_y = dataset[:, 0]
    # test data
    dataframe = pandas.read_csv(test_path)
    dataframe.pop('name')
    dataset = dataframe.values
    test_x = dataset[:, 1:7]
    test_y = dataset[:, 0]

    return train_x, train_y, test_x, test_y

    # baseline model

def create_baseline():
    # create model
    model = Sequential()
    model.add(Dense(24, input_dim=6, kernel_initializer='normal', activation='relu'))
    model.add(Dense(12, kernel_initializer='normal', activation='relu'))
    model.add(Dense(1, kernel_initializer='normal', activation='sigmoid'))
    # Compile model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

def train_model(model):
    train_x, train_y, test_x, test_y = getData()
    model.fit(train_x, train_y, epochs=20, batch_size=50, verbose=1)
    return model

def evaluate():
    seed = 7
    numpy.random.seed(seed)
    # evaluate model with standardized dataset
    estimator = KerasClassifier(build_fn=create_baseline, epochs=100, batch_size=5, verbose=0)
    kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=seed)
    results = cross_val_score(estimator, train_x, train_y, cv=kfold)
    print("Results: %.2f%% (%.2f%%)" % (results.mean() * 100, results.std() * 100))

tes= {
  "favourites": 0,
  "followers": 50006160,
  "following": 45,
  "moments": 6,
  "tweets": 37245,
  "verified": 1
}

model = train_model(create_baseline())

data = pandas.DataFrame(tes, index=[6])
data = data.values
prediction, probability = model.predict_classes(data), model.predict(data)
probability = probability * 100
print(prediction)
print(probability)



