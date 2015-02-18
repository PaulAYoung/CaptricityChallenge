#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
from datetime import date
from os import path
from uuid import uuid4

from flask import (Blueprint,
                   current_app,
                   render_template,
                   request,
                   send_from_directory,
                   flash,
                   redirect,
                   url_for,
                   jsonify)

from flask.ext.login import (login_user,
                            logout_user,
                            current_user,
                            login_required)

from sqlalchemy.exc import IntegrityError
from werkzeug import secure_filename

from captricity.models import User, Batch, Image, db_session

image_views = Blueprint('image_views', __name__, static_folder= "static", template_folder= "templates")

allowed_extensions = ['.jpg', ',jpeg', '.png', '.gif', '.pdf', '.tiff']

# regex to check if a file's title is valid
title_validator = re.compile(r"^[a-zA-Z0-9 ._-]+$")


def get_unique_filename(fname, fdir):
    """
    Generates a unique filename.

    params:
    fname - original filename, used to get extension
    fdir - makes sure file does not exist in this directory.
    """
    ext = path.splitext(fname)[1]

    while True:
        uid = uuid4().hex
        name = uid + ext
        if not path.exists(path.join(fdir, name)):
            return name


def check_file_type(fname):
    """
    Checks if extension of fname is allowed
    """
    ext = path.splitext(fname)[1]
    return ext in allowed_extensions

############################################
# image related views
###########################################


@image_views.route('/upload', methods=['POST'])
def upload_post():
    "handles image uploads"
    file = request.files["file"]
    title = request.form["title"]
    error = False

    if not title:
        title = file.filename

    if not title_validator.match(title):
        flash("{} is not a valid title.".format(title), "error")
        error = True

    if (not check_file_type(file.filename)) or (not file):
        flash("Invalid file given.", "error")
        error = True
        
    user = current_user.id

    if not error:
        outdir = current_app.config['UPLOAD_FOLDER']
        fname = get_unique_filename(secure_filename(file.filename), outdir)
        fpath = path.join(outdir, fname)
        file.save(fpath)

        # add to db
        image = Image(title=title, path=fname, user=user)
        db_session.add(image)
        db_session.commit()

        flash("{} uploaded succesfully.".format(title))

    return render_template('upload.html')


@image_views.route('/upload')
@login_required
def upload():
    return render_template('upload.html')


@image_views.route('/rawimage/<image_path>')
def raw_image(image_path):
    image_dir = current_app.config['UPLOAD_FOLDER']
    return send_from_directory(image_dir, image_path)


@image_views.route('/viewimage/<image_id>')
def view_image(image_id):
    image = Image.query.filter(Image.id==image_id).first()
    return render_template('viewimage.html', image=image)


@image_views.route('/api/images')
@login_required
def image_api():
    """
    Returns json feed of user images
    """
    PAGE_SIZE=50
    page = int(request.args.get('page', 0))
    print page
    userid = current_user.id
    out= []
    query = db_session.query(Image, Batch.status).\
            outerjoin(Batch, Image.batch==Batch.batch_id).\
            filter(Image.user==userid)

    count = query.count()
    for row in query.limit(PAGE_SIZE).offset(page*PAGE_SIZE):
        out.append({
            "url": url_for('image_views.raw_image', image_path=row.Image.path),
            "page": url_for('image_views.view_image', image_id=row.Image.id),
            "title": row.Image.title,
            "status": row.status
            })

    return jsonify({"images": out, "count": count})


@image_views.route('/api/images/delete/<int:image_id>')
@login_required
def delete_image(image_id):
    image = Image.query.\
                        filter(Image.id==image_id).\
                        filter(Image.user==current_user.id).\
                        first()

    if image:
        outdir = current_app.config['UPLOAD_FOLDER']
        fpath = path.join(outdir, image.path)
        db_session.delete(image)
        if path.exists(fpath):
            os.remove(fpath)
        db_session.commit()
        flash("{} deleted".format(image.title))
        return redirect(url_for('image_views.my_images'))
    else:
        flash("{} could not be deleted".format(image.title))
        return redirect(url_for('image_views.my_images'))


@image_views.route('/myimages/<page>')
@image_views.route('/myimages', defaults={'page': 0})
@login_required
def my_images(page):
    return render_template('myimages.html', page=page)
