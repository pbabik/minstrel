#!/usr/bin/python
# -*- coding: utf-8 -*-

import PIL
from PIL import Image
import StringIO
import os.path as op
import uuid

from app import app
from auth import *

ALLOWED_EXTENSIONS = set(['jpg','JPG','JPEG','jpeg','gpx','GPX'])
UPLOAD_FOLDER = op.join(op.dirname('__file__'),'uploads')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def generate_file_name(old_name):
    extension = old_name.rsplit('.', 1)[1]
    new_name = str(uuid.uuid4()).split('-')[4]+'.'+extension
    return new_name

def save_file(a_file,new_name,destination): 
    fullpath = op.join(UPLOAD_FOLDER, destination, new_name)
    a_file.save(fullpath)
    return new_name

def handle_photo(a_photo):
    im = Image.open(a_photo)
    im.thumbnail((800,600), Image.ANTIALIAS)
    new_name = generate_file_name(a_photo.filename)
    im.save(op.join(UPLOAD_FOLDER,'photos',new_name))
    im.thumbnail((100,100), Image.ANTIALIAS)
    im.save(op.join(UPLOAD_FOLDER,'thumbs',new_name))
    latlng = geom_from_exif(im)
    return {'user':auth.get_logged_in_user(),'url':'media/photos/%s' % new_name, 'thumbnail': 'media/thumbs/%s' % new_name, 'caption': '', 'lat': latlng[0], 'lng': latlng[1]}
    

def handle_photos(a_list):
    results = []
    for photo in a_list:
        results.append(handle_photo(photo))
    return results

def handle_track(a_track):
    old_name = a_track.filename
    new_name = generate_file_name(old_name)
    return save_file(a_track,new_name,'tracks')

def geom_from_exif(an_image):
    from get_lat_lon_exif_pil import get_exif_data,get_lat_lon
    the_exif = get_exif_data(an_image)
    latlon = get_lat_lon(the_exif)	
    return latlon
