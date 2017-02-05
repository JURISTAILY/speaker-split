from flask import Flask, request, jsonify
from flask_cors import CORS as Cors
from flask_restful import Api, Resource

APPLICATION_ROOT = '/api'
RESTFUL_JSON = {
    'ensure_ascii': False,
    'sort_keys': True,
    'indent': 4,
}

app = Flask(__name__)
app.config.from_object(__name__)
api = Api(app)
cors = Cors(app, resources={
    '/*': {'origins': '*'},
})


CALL = {
    "id": 157,
    "date": "2017-01-22H22:30:21+03:00",
    "duration": 31.2,
    "grade": 7.2,
    "isIncoming": True,
    "info": {
        "quantitative_timing": {
            "grade": 6.9,
            "params": [
                {"name": "operator_speech_ratio", "value": 0.7, "grade": 4.9},
                {"name": "operator_speech_duration", "value": 24.0, "grade": 9.1},
                {"name": "operator_interruptions", "value": 4, "grade": 2},
            ],
        },
        "speech_activity": [],
        "semantic": [],
        "emotional": [],
    },
    "transcript": [
        {"speaker": "operator", "begin": 0.3, "end": 1.2, "phrase": "Здравствуйте! вы насчет работы торговым представителем?"},
        {"speaker": "client", "begin": 1.7, "end": 2.9, "phrase": "Да, вот моё резюме."},
        {"speaker": "operator", "begin": 4.3, "end": 7.2, "phrase": "В нашей компании ассортимент товаров, с которыми вам придется работать, будет намного шире. Это кондитерские изделия: торты, пирожные, рулетики, конфеты. На какую зарплату вы рассчитываете?"},
        {"speaker": "client", "begin": 8.3, "end": 11.2, "phrase": "На пятьсот долларов, как указано в вашем объявлении. Еще я рассчитываю, что если буду хорошо справляться со своими обязанностями, моя зарплата вырастет."},
        {"speaker": "operator", "begin": 12.3, "end": 14.2, "phrase": "Наша компания всегда поощряет сотрудников за успехи в труде. Скажите, почему вы выбрали для работы именно нашу компанию?"},
    ],
}



class CallResource(Resource):
    def get(self):
        calls = [CALL.copy() for _ in range(3)]
        for n, _ in enumerate(calls):
            calls[n]['id'] = 157 + n
        return dict(data=calls)


api.add_resource(CallResource, '/calls')


@app.errorhandler(404)
def page_not_found(e):
    return jsonify(info=str(request))


if __name__ == '__main__':
    app.run(port=8001, debug=True)
