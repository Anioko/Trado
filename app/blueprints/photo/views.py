from flask import (Blueprint, flash, redirect, render_template, request,
                   url_for)
from flask_login import current_user, login_required
from typing import List
from app import db, images
from app.blueprints.photo.forms import ImageForm
from app.models import Photo

photo = Blueprint('photo', __name__)


@photo.route('/index')
@login_required
def index():
    return render_template('photo/index.html')


@photo.route('/add', methods=['POST', 'GET'])
@login_required
def add_photo():
    form = ImageForm()
    count = Photo.query.filter_by(user_id=current_user.id).count()
    if count >= 5:
        return redirect(url_for('photo.added_images'))
    if form.validate_on_submit():
        data = Photo(
            image = images.save(request.files['image']),
            profile_picture = form.profile_picture.data,
            user_id = current_user.id
            )
        db.session.add(data)
        db.session.commit()
        flash("Picture Added Successfully.", "success")
        return redirect(url_for('photo.show', id=data.id))
    return render_template('photo/add_photo.html', form=form)


@photo.route('/', methods=['POST', 'GET'])
@login_required
def added_images():
    """View added images."""
    count = Photo.query.filter_by(user_id=current_user.id).count()
    photo_data = Photo.query.filter_by(user_id=current_user.id).all()
    if photo_data is None:
        return redirect(url_for('photo.add_photo'))

    form = ImageForm()
    count = Photo.query.filter_by(user_id=current_user.id).count()
    if count >= 5:
        return redirect(url_for('photo.added_images'))
    if form.validate_on_submit():
        data = Photo(
            image = images.save(request.files['image']),
            profile_picture = form.profile_picture.data,
            user_id = current_user.id
            )
        db.session.add(data)
        db.session.commit()
        flash("Picture Added Successfully.", "success")
        return redirect(url_for('photo.show', id=data.id))
    
    return render_template(
        'socialite/photo.html', photo_data=photo_data, count=count, form=form)

@photo.route('/<id>')
@login_required
def added_image(id):
    """View added image."""
    data = Photo.query.filter_by(id=id).first()
    return render_template(
        'photo/added_image.html', data=data)

@photo.route('/<id>')
@login_required
def show(id):
    """View added image."""
    data = Photo.query.filter_by(id=id).first()
    if data is None:
        return redirect(url_for('photo.add_photo'))
    return render_template(
        'photo/added_images.html', data=data, photo=Photo())

@photo.route('/<int:id>/_delete', methods=['GET', 'POST'])
@login_required
def delete_photo(id):
    """Delete the image added """
    data = Photo.query.filter_by(id=id).first()
    db.session.commit()
    db.session.delete(data)
    flash('Successfully deleted ' , 'success')
    if data is None:
        return redirect(url_for('photo.upload'))
    return redirect(url_for('photo.added_images'))
