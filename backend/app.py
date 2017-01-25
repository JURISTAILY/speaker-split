# from flask import Flask
import flask

app = flask.Flask(__name__)


@app.route('/api/calls')
def show_calls():
    calls = []
    return flask.jsonify(calls=calls)


if __name__ == '__main__':
    app.run('localhost', port=8001, debug=True)
