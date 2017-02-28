import functools
import itertools

from sqlalchemy import (
    Column as BaseColumn, Unicode,
    Integer, ForeignKey, Float, Boolean, UnicodeText,
)
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ArrowType
from flask import Flask, request, jsonify, send_from_directory, abort
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
import flask_cors
import arrow

Column = functools.partial(BaseColumn, nullable=False)


APPLICATION_ROOT = '/api'
RESTFUL_JSON = {
    'ensure_ascii': False,
    'sort_keys': True,
    'indent': 4,
}
SQLALCHEMY_DATABASE_URI = 'postgresql://speaker:deQucRawR27U@194.58.103.124/speaker-db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

DEFAULT_TRANSCRIPT = [
    {"speaker": "operator", "begin": 0.3, "end": 1.2, "phrase": "Здравствуйте! вы насчет работы торговым представителем?"},
    {"speaker": "client", "begin": 1.7, "end": 2.9, "phrase": "Да, вот моё резюме."},
    {"speaker": "operator", "begin": 4.3, "end": 7.2, "phrase": "В нашей компании ассортимент товаров, с которыми вам придется работать, будет намного шире. Это кондитерские изделия: торты, пирожные, рулетики, конфеты. На какую зарплату вы рассчитываете?"},
    {"speaker": "client", "begin": 8.3, "end": 11.2, "phrase": "На пятьсот долларов, как указано в вашем объявлении. Еще я рассчитываю, что если буду хорошо справляться со своими обязанностями, моя зарплата вырастет."},
    {"speaker": "operator", "begin": 12.3, "end": 14.2, "phrase": "Наша компания всегда поощряет сотрудников за успехи в труде. Скажите, почему вы выбрали для работы именно нашу компанию?"},
]

RECORDINGS_DIR = 'audio_samples'
MIMETYPES = {
    'wav': 'audio/wav',
    'mp3': 'audio/mpeg',
}


app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)
rest_api = Api(app)
cors = flask_cors.CORS(app, resources={'/*': {'origins': '*'}})


class PrimaryKeyMixin:
    id = Column(Integer, primary_key=True)


class Call(db.Model, PrimaryKeyMixin):
    __tablename__ = 'calls'

    date = Column(ArrowType(timezone=True), default=arrow.now)
    duration = Column(Float)
    is_incoming = Column(Boolean)
    recording_filename = Column(Unicode)

    parameters = relationship('Parameter', lazy='joined', order_by='Parameter.id')

    @classmethod
    def add_new(cls, data):
        try:
            call = cls(
                duration=data['duration'],
                is_incoming=data['is_incoming'],
                recording_filename=data['filename'],
            )

            db.session.add(call)
            db.session.flush()

            for name, value in data['info'].items():
                meta = db.session.query(ParameterMeta).filter_by(name=name).one()
                db.session.add(Parameter(call_id=call.id,
                                         parameter_meta_id=meta.id,
                                         value=value))
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    def json(self):

        def gen_key(p):
            return p.meta.category.name

        items = [
            {
                'name': key,
                'grade': 0.0,
                'params': [p.json() for p in group],
            }
            for key, group in itertools.groupby(
                sorted(self.parameters, key=gen_key), key=gen_key)
        ]

        def generate_info():
            for c in Category.get_all():
                piece = {'name': c.name, 'name_rus': c.name_rus, 'grade': 0.0, 'params': []}
                for item in items:
                    if item['name'] == piece['name']:
                        piece.update(item)
                        break
                yield piece

        return {
            'id': self.id,
            'date': str(self.date),
            'duration': self.duration,
            'isIncoming': True,
            'transcript': DEFAULT_TRANSCRIPT,
            'info': list(generate_info()),
        }

    def __repr__(self):
        return '<Call (id={}, duration={}, date="{}")>'.format(
            self.id, self.duration, self.date)


class Category(db.Model, PrimaryKeyMixin):
    __tablename__ = 'categories'

    name = Column(Unicode, unique=True)
    name_rus = Column(Unicode, unique=True)

    @classmethod
    def get_all(cls):
        return db.session.query(cls).order_by(cls.id).all()


class ParameterMeta(db.Model, PrimaryKeyMixin):
    __tablename__ = 'parameters_meta'

    name = Column(Unicode, unique=True)
    name_rus = Column(Unicode)
    description = Column(UnicodeText, default='')
    category_id = Column(Integer, ForeignKey('categories.id'))

    category = relationship('Category', lazy='joined')


class Parameter(db.Model, PrimaryKeyMixin):
    __tablename__ = 'parameters'

    parameter_meta_id = Column(Integer, ForeignKey('parameters_meta.id', ondelete='CASCADE'))
    value = Column(Float)

    # If corresponding call is deleted,
    # all associated parameters will also be deleted
    # by PostgreSQL following the `ON DELETE CASCADE`
    # DDL instruction, defined at table creation time.
    call_id = Column(Integer, ForeignKey('calls.id', ondelete='CASCADE'))

    meta = relationship('ParameterMeta', lazy='joined')

    def json(self):
        return {
            'id': self.meta.id,
            'name': self.meta.name,
            'name_rus': self.meta.name_rus,
            'value': self.value
        }

    def __repr__(self):
        return "<Parameter ('{}', {})>".format(self.meta.name_rus, self.value)


class CallResource(Resource):
    def get(self):
        data = {
            'data': [
                call.json() for call in db.session.query(Call)
                                                  .order_by(Call.date.desc())
                                                  .all()
            ]
        }
        headers = {'Cache-Control': 'no-cache, must-revalidate'}
        return data, 200, headers


rest_api.add_resource(CallResource, '/calls')


@app.route('/recordings/<int:call_id>')
def serve_recording(call_id):
    call = db.session.query(Call.recording_filename).filter_by(id=call_id).first()

    if call is None:
        abort(404)

    if call.recording_filename.endswith('.mp3'):
        mimetype = MIMETYPES['mp3']
    elif call.recording_filename.endswith('.wav'):
        mimetype = MIMETYPES['wav']
    else:
        raise RuntimeError(
            'Unsupported recording file extension ({}) (call_id={}).'
            .format(call.recording_filename, call_id)
        )

    return send_from_directory(RECORDINGS_DIR, call.recording_filename,
                               mimetype=mimetype)


if __name__ == '__main__':
    app.run(port=8001, debug=True)
