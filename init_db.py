#!/usr/bin/python
# -*- coding: utf-8 -*-

from models import User,Photo,Album
from app import app

User.create_table()
Photo.create_table()
Album.create_table()