#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import os
from time import time
import datetime
from functools import wraps, update_wrapper
from flask import Flask, g, render_template, session, request, jsonify, redirect, url_for, make_response
from flask_peewee.db import Database
import config


app = Flask(__name__)
app.config.from_object('config.Configuration')
db = Database(app)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5007)
