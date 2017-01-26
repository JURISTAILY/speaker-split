from flask import Flask, request, jsonify

APPLICATION_ROOT = '/api'

app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/calls')
def show_calls():
    calls = []
    return jsonify(calls=calls)


@app.errorhandler(404)
def page_not_found(e):
    return jsonify(info=str(request))


if __name__ == '__main__':
    app.run('localhost', port=8001, debug=True)
