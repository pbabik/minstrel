from app import app, db

from auth import *
from models import *
from routes import *

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5007)
