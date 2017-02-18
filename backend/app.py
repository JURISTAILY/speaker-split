from flask import Flask, request, jsonify
from flask_cors import CORS as Cors
from flask_restful import Api, Resource
import functools

from sqlalchemy import (
    Column as BaseColumn, Unicode,
    Integer, ForeignKey, Float, Boolean,
)
from sqlalchemy_utils import ArrowType
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

import arrow

APPLICATION_ROOT = '/api'
RESTFUL_JSON = {
    'ensure_ascii': False,
    'sort_keys': True,
    'indent': 4,
}
SQLALCHEMY_DATABASE_URI = 'postgresql://speaker:deQucRawR27U@194.58.103.124/speaker-db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__)
app.config.from_object(__name__)
api = Api(app)
cors = Cors(app, resources={
    '/*': {'origins': '*'},
})

db = SQLAlchemy(app)


Column = functools.partial(BaseColumn, nullable=False)


class WithId:
    id = Column(Integer, primary_key=True)


class Call(db.Model, WithId):
    __tablename__ = 'calls'

    date = Column(ArrowType(timezone=True), default=arrow.now)
    duration = Column(Float)
    is_incoming = Column(Boolean)

    parameter_values = relationship('ParameterValue')

    def as_json(self):
        return {}

    def __repr__(self):
        return '<Call id={}, duration={}, date={}>'.format(self.id, self.duration, self.date)


class Category(db.Model, WithId):
    __tablename__ = 'categories'

    name = Column(Unicode, unique=True)
    parameters = relationship('Parameter', back_populates='category')


class Parameter(db.Model, WithId):
    __tablename__ = 'parameters'

    name = Column(Unicode, unique=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', back_populates='parameters')


class ParameterValue(db.Model, WithId):
    parameter_id = Column(Integer, ForeignKey('parameters.id'))
    value = Column(Float)
    call_id = Column(Integer, ForeignKey('calls.id'))


def init_db():

    try:
        c = db.session.query(Category).filter_by(name='quantitive_timing').one()

        db.session.add(Parameter(name="operator_speech_ratio", category=c))
        db.session.add(Parameter(name="operator_speech_duration", category=c))
        db.session.add(Parameter(name="operator_interruptions", category=c))

        db.session.commit()

        call = Call(duration=12.4, is_incoming=True)
        db.session.add(call)
        db.session.flush()

        db.session.add(ParameterValue(call_id=call.id, parameter_id=1, value=0.7))
        db.session.add(ParameterValue(call_id=call.id, parameter_id=2, value=24.0))
        db.session.add(ParameterValue(call_id=call.id, parameter_id=3, value=4.0))

        db.session.flush()

        db.session.commit()

    except Exception:
        db.session.rollback()
        raise



CALL = {
    "id": 157,
    "date": "2017-01-22H22:30:21+03:00",
    "duration": 31.2,
    "grade": 7.2,
    "isIncoming": True,
    "info": [
        {
            "name" : "quantitative_timing",
            "grade": 6.9,
            "params": [
                {"name": "operator_speech_ratio", "value": 0.7, "grade": 4.9},
                {"name": "operator_speech_duration", "value": 24.0, "grade": 9.1},
                {"name": "operator_interruptions", "value": 4, "grade": 2},
            ],
        },
        {
            "name" : "speech_activity"
        },
        {
            "name" : "semantic"
        },
        {
            "name" : "emotional"
        }
    ],
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
        # calls = db.session.query(Call).order_by(Call.date.desc()).all()
        # return {'data': [call.as_json() for call in calls]}
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
