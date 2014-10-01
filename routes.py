import datetime
import os
import os.path as op
from flask import request, redirect, url_for, render_template, flash, g, jsonify, send_from_directory,abort
import json

from flask_peewee.utils import get_object_or_404, object_list
import peewee 

from app import app, db
from auth import auth
from models import User, Album, Photo
from file_handler import handle_photos, handle_track

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

def insert_photos(req,album):
    if req.files.getlist('photos'):
        fotoz = req.files.getlist('photos')
    else:
        fotoz = [req.files.get('photos', None)]
    foto_list = handle_photos(fotoz)
    for foto in foto_list:
	    foto['album'] = album
    Photo.insert_many(foto_list).execute()		

@app.route('/albums', methods=['GET','POST'])
def albums():
    current_user = auth.get_logged_in_user()
    if request.method == 'GET':
        my_albums = {'albums': []}		
        data = Album.select().where(Album.user==current_user).dicts()
        for row in data:
            cover = Photo.select().where(Photo.album == row['id']).get()
            row['cover'] = cover.url
            my_albums['albums'].append(row)
        return jsonify(my_albums)
    else:
        if request.files.get('track'):
            track = handle_track(request.files.get('track'))
        else:
            track = ''
        new_album = Album(user=current_user,title=request.form.get('title'),has_elevation=True,basemap=request.form.get('basemap'),track=track)
        new_album.save()
        insert_photos(request,new_album)
        return jsonify({'Created':new_album.id}),201    
    
@app.route('/albums/<albumid>',methods=['GET','POST','PUT','DELETE'])
@auth.login_required
def album(albumid):
    try:
        the_album = Album.get(Album.id==albumid)
    except:
        abort(404)		
    if request.method == 'GET':
        resp = {'id':the_album.id,'title':the_album.title,'has_elevation': the_album.has_elevation,
                 'basemap':the_album.basemap,'track':the_album.track,'photos':[]}
        album_photos = Photo.select().where(Photo.album==the_album).dicts()
        for row in album_photos:
            resp['photos'].append(row)
        return jsonify(resp)
    elif request.method == 'POST':
        insert_photos(request,the_album)
        return jsonify({'Updated':albumid})      
    elif request.method == 'PUT':
        newdata = request.get_json(force=True)
        the_album.title = newdata['title']
        the_album.has_elevation = newdata['has_elevation']
        the_album.basemap = newdata['basemap']
        the_album.save()
        return jsonify({'updated':albumid}) 
    else:
        album_photos = Photo.select(Photo.album==the_album)
        for row in album_photos:
            try:
                ph = op.join(dirname(__file__),app.config['UPLOAD_FOLDER'],'photos',row.url.split('/')[2])
                th = op.join(dirname(__file__),app.config['UPLOAD_FOLDER'],'thumbs',row.url.split('/')[2])			
                os.remove(ph) if op.exists(ph) else None
                os.remove(th) if op.exists(th) else None
            except:
                pass				
            row.delete_instance()
        the_album.delete_instance()
        return jsonify({'deleted':albumid})


@app.route('/photos/<photoid>',methods=['GET','PUT','DELETE'])
@auth.login_required
def photo(photoid):
    the_photo = get_object_or_404(Photo, Photo.id==photoid)
    if request.method == 'GET':
        return jsonify({'id':the_photo.id,'lat':the_photo.lat,'lng':the_photo.lng,'url':the_photo.url,'caption':the_photo.caption,'thumbnail':the_photo.thumbnail})
    elif request.method == 'PUT':
        newdata = request.get_json(force=True)
        the_photo.caption = newdata['caption']
        the_photo.lat = newdata['lat']
        the_photo.lng = newdata['lng']
        the_photo.save()
        return jsonify({'updated':photoid})
    else:
        os.unlink(op.join(op.dirname(__file__),app.config['UPLOAD_FOLDER'],'photos',the_photo.url.split('/')[2]))
        os.unlink(op.join(dirname(__file__),app.config['UPLOAD_FOLDER'],'photos',the_photo.url.split('/')[2]))
        the_photo.delete_instance()
        return jsonify({'deleted':photoid})

@app.route('/map/<mapid>')
def map(mapid):
    the_album = Album.get(Album.id==mapid)
    return render_template('map.html',album=the_album)
    
@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'POST' and request.form['username']:
        try:
            user = User.select().where(User.username==request.form['username']).get()
            flash('That username is already taken')
        except User.DoesNotExist:
            user = User(
                username=request.form['username'],
                email=request.form['email'],
                join_date=datetime.datetime.now()
            )
            user.set_password(request.form['password'])
            user.save()
            auth.login_user(user)
            return redirect(url_for('dashboard'))

    return render_template('join.html')

@app.route('/media/<filetype>/<filename>')
def send_media(filetype,filename):
    return send_from_directory(op.join(app.config['UPLOAD_FOLDER'],filetype),filename)
