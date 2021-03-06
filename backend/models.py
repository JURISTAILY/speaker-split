import functools
import itertools
import json

from sqlalchemy import (
    Column as BaseColumn, Unicode, JSON,
    Integer, ForeignKey, Float, Boolean, UnicodeText,
)
from flask import Flask
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ArrowType
from flask_sqlalchemy import SQLAlchemy
import arrow

app = Flask(__name__)
app.config.from_object('settings')

Column = functools.partial(BaseColumn, nullable=False)


class SQLAlchemyCustomized(SQLAlchemy):
    def apply_driver_hacks(self, app, info, options):
        SQLAlchemy.apply_driver_hacks(self, app, info, options)
        # Option relevant only for psycopg2 driver.
        # See SQLAlchemy docs on PostgreSQL for reference.
        # It is passed as parameter to psycopg2's create_engine.
        options['json_serializer'] = functools.partial(
            json.dumps, **app.config.get('POSTGRESQL_JSON', {}))


db = SQLAlchemyCustomized(app)


class PrimaryKeyMixin:
    id = Column(Integer, primary_key=True)


class Call(db.Model, PrimaryKeyMixin):
    __tablename__ = 'calls'

    date = Column(ArrowType(timezone=True), default=arrow.now)
    duration = Column(Float)
    is_incoming = Column(Boolean)
    recording_filename = Column(Unicode)
    transcript = Column(JSON, server_default='[]')

    parameters = relationship('Parameter', lazy='joined', order_by='Parameter.id')

    @classmethod
    def add_new(cls, data, transcript):
        try:
            call = cls(
                duration=data['duration'],
                is_incoming=data['is_incoming'],
                recording_filename=data['filename'],
                transcript=transcript,
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
                piece = {
                    'name': c.name, 'name_rus': c.name_rus,
                    'grade': 0.0, 'params': [],
                    }
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
            'transcript': self.transcript,
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
    description = Column(UnicodeText, server_default='')
    category_id = Column(Integer, ForeignKey('categories.id'))

    category = relationship('Category', lazy='joined')


class Parameter(db.Model, PrimaryKeyMixin):
    __tablename__ = 'parameters'

    parameter_meta_id = Column(Integer, ForeignKey('parameters_meta.id',
                                                   ondelete='CASCADE'))
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
