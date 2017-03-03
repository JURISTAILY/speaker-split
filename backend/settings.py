APPLICATION_ROOT = '/api'
RESTFUL_JSON = {
    'ensure_ascii': False,
    'sort_keys': True,
    'indent': 4,
}
POSTGRESQL_JSON = {**RESTFUL_JSON, 'indent': 2}
SQLALCHEMY_DATABASE_URI = 'postgresql://speaker:deQucRawR27U@194.58.103.124/speaker-db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
DEBUG = False
MIMETYPES = {
    '.wav': 'audio/wav',
    '.mp3': 'audio/mpeg',
}
