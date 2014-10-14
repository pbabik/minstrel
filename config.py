# config
import os.path as op

class Configuration(object):
    DATABASE = {
        'name': 'minstrel.db',
        'engine': 'peewee.SqliteDatabase',
        'check_same_thread': False,
    }
    DEBUG = True
    SECRET_KEY = 'EP09-005+B+B+Bh+Bh+B+WR+A+A'
    UPLOAD_FOLDER = op.join(op.dirname('__file__'),'uploads')
    BASE_URL = 'http://127.0.0.1:5007'
