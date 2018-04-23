from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from flask import Flask, jsonify
import scrape
import argparse
import tensorflow as tf
import take_in_data
import scrape
import Mongo2

app = Flask(__name__)
init = False
parser = argparse.ArgumentParser()
parser.add_argument('--batch_size', default=100, type=int, help='batch size')
parser.add_argument('--train_steps', default=1000, type=int,
                    help='number of training steps')

classifier = None

def my_model(features, labels, mode, params):
    """DNN with three hidden layers, and dropout of 0.1 probability."""
    # Create three fully connected layers each layer having a dropout
    # probability of 0.1.
    net = tf.feature_column.input_layer(features, params['feature_columns'])
    for units in params['hidden_units']:
        net = tf.layers.dense(net, units=units, activation=tf.nn.relu)

    # Compute logits (1 per class).
    logits = tf.layers.dense(net, params['n_classes'], activation=None)

    # Compute predictions.
    predicted_classes = tf.argmax(logits, 1)
    if mode == tf.estimator.ModeKeys.PREDICT:
        predictions = {
            'class_ids': predicted_classes[:, tf.newaxis],
            'probabilities': tf.nn.softmax(logits),
            'logits': logits,
        }
        return tf.estimator.EstimatorSpec(mode, predictions=predictions)

    # Compute loss.
    loss = tf.losses.sparse_softmax_cross_entropy(labels=labels, logits=logits)

    # Compute evaluation metrics.
    accuracy = tf.metrics.accuracy(labels=labels,
                                   predictions=predicted_classes,
                                   name='acc_op')
    metrics = {'accuracy': accuracy}
    tf.summary.scalar('accuracy', accuracy[1])

    if mode == tf.estimator.ModeKeys.EVAL:
        return tf.estimator.EstimatorSpec(
            mode, loss=loss, eval_metric_ops=metrics)

    # Create training op.
    assert mode == tf.estimator.ModeKeys.TRAIN

    optimizer = tf.train.AdagradOptimizer(learning_rate=0.1)
    train_op = optimizer.minimize(loss, global_step=tf.train.get_global_step())
    return tf.estimator.EstimatorSpec(mode, loss=loss, train_op=train_op)

def main(argv):
    global classifier
    args = parser.parse_args(argv[1:])

    # Fetch the data
    (train_x, train_y), (test_x, test_y) = take_in_data.load_data()

    # Feature columns describe how to use the input.
    my_feature_columns = []
    for key in train_x.keys():
        my_feature_columns.append(tf.feature_column.numeric_column(key=key))

    # Build 2 hidden layer DNN with 10, 10 units respectively.
    classifier = tf.estimator.Estimator(
        model_fn=my_model,
        params={
            'feature_columns': my_feature_columns,
            # Two hidden layers of 10 nodes each.
            'hidden_units': [10, 10],
            # The model must choose between 3 classes.
            'n_classes': 3,
        })

    # Train the Model.
    classifier.train(
        input_fn=lambda: take_in_data.train_input_fn(train_x, train_y, args.batch_size),
        steps=args.train_steps)

    # Evaluate the model.
    eval_result = classifier.evaluate(
        input_fn=lambda: take_in_data.eval_input_fn(test_x, test_y, args.batch_size))

    print('\nTest set accuracy: {accuracy:0.3f}\n'.format(**eval_result))

    # Start the server

    app.run(debug=True)

##Evaluate is used on newly scraped data
def evaluate(data):
    data = {k:[v] for (k,v) in zip(data.keys(),data.values())}

    prediction = classifier.predict(input_fn=lambda: take_in_data.eval_input_fn(data,
                                                                                labels=None,
                                                                                batch_size=100))

    x = next(prediction)
    classification = x['class_ids'][0]
    probability = x['probabilities'][classification] *100
    what= take_in_data.SPECIES[classification]
    return what,probability

@app.route('/<string:name>')
def evaluateName(name):
    ##First query the db
    x = Mongo2.queryUname(name)
    ##If db returns nothing
    if x is None:
        data = scrape.getName(name)
        if data is None:
            data = {'name':'Does not exist'}
            return jsonify(data)
        data.pop('name')
        botvalue,probability = evaluate(data)
        data['bot'],data['probability'],data['name'] = botvalue, probability, name
        Mongo2.insertOrUpdate(data)
        data.pop('_id')

    else:
        data = x

    return jsonify(data)

@app.route('/listBots')
def listBots():
    x = Mongo2.listBots()
    print(x)
    return jsonify(x)


if __name__ == '__main__':
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run(main)
