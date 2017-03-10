import os.path

RESTFUL_JSON = {
    'ensure_ascii': False,
    'sort_keys': True,
    'indent': 4,
}
POSTGRESQL_JSON = RESTFUL_JSON.copy()
POSTGRESQL_JSON['indent'] = 2
SQLALCHEMY_DATABASE_URI = 'postgresql://speaker:deQucRawR27U@194.58.103.124/speaker-db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False
DEBUG = False
MIMETYPES = {
    '.wav': 'audio/wav',
    '.mp3': 'audio/mpeg',
}
PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))
RECORDINGS_DIR = os.path.join(PROJECT_DIR, 'audio_samples')
