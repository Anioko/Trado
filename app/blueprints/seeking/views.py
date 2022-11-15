from flask import (Blueprint, flash, redirect, render_template,
                   url_for)
from flask_login import current_user, login_required

from app import db
from app.blueprints.seeking.forms import SeekingForm
from app.models import Seeking, User


seeking = Blueprint('seeking', __name__)


@seeking.route('/index')
@login_required
def index():
    return render_template('seeking/index.html')


# View preference
@seeking.route('/<int:id>/<username>/added', methods=['POST', 'GET'])
@login_required
def added_preference(id, username):
    """View added preference."""
    user = db.session.query(User).filter(User.id == id,
                                         User.username == username).first()
    data = Seeking.query.filter_by(user_id=id).first()
    if current_user and data is None:
        return redirect(
            url_for('seeking.add_preference', id=id, username=username))
    return render_template('seeking/added_preference.html',
                           data=data,
                           id=id,
                           username=username,
                           user=user)


@seeking.route('/<int:id>/<username>/add', methods=['POST', 'GET'])
@login_required
def add_preference(id, username):
    """Add prefence function for users """

    if current_user.id != id and current_user.username != username:
        return redirect(
            url_for('seeking.add_preference',
                    id=current_user.id,
                    username=current_user.username))
    elif id != current_user.id:
        return redirect(
            url_for('seeking.add_preference',
                    id=current_user.id,
                    username=current_user.username))
    data = Seeking.query.filter_by(user_id=id).first()
    if data:
        return redirect(
            url_for('seeking.added_preference',
                    id=current_user.id,
                    username=current_user.username))

    form = SeekingForm()
    if form.validate_on_submit():
        seeking = Seeking(
            user_id=current_user.id,
            seeking_partner=form.seeking_partner.data,
            seeking_from_height=form.seeking_from_height.data,
            seeking_to_height=form.seeking_to_height.data,
            seeking_sex=form.seeking_sex.data,
            seeking_from_age=form.seeking_from_age.data,
            seeking_to_age=form.seeking_to_age.data,
            seeking_country_one=form.seeking_country_one.data,
            seeking_country_two=form.seeking_country_two.data,
            seeking_country_three=form.seeking_country_three.data,
            seeking_country_four=form.seeking_country_four.data,
            seeking_country_five=form.seeking_country_five.data,
            seeking_country_six=form.seeking_country_six.data,
            seeking_country_seven=form.seeking_country_seven.data,
            seeking_country_eight=form.seeking_country_eight.data,
            seeking_religion_one=form.seeking_religion_one.data,
            seeking_religion_two=form.seeking_religion_two.data,
            seeking_religion_three=form.seeking_religion_three.data,
            seeking_ethnicity_one=form.seeking_ethnicity_one.data,
            seeking_ethnicity_two=form.seeking_ethnicity_two.data,
            seeking_ethnicity_three=form.seeking_ethnicity_three.data,
            seeking_ethnicity_four=form.seeking_ethnicity_four.data,
            seeking_ethnicity_five=form.seeking_ethnicity_five.data,
            seeking_marital_type_one=form.seeking_marital_type_one.data,
            seeking_body_type_one=form.seeking_body_type_one.data,
            seeking_body_type_two=form.seeking_body_type_two.data,
            seeking_body_type_three=form.seeking_body_type_three.data,
            seeking_body_type_four=form.seeking_body_type_four.data,
            seeking_church_denomination_one=form.
            seeking_church_denomination_one.data,
            seeking_church_denomination_two=form.
            seeking_church_denomination_two.data,
            seeking_church_denomination_three=form.
            seeking_church_denomination_three.data,
            seeking_church_denomination_four=form.
            seeking_church_denomination_four.data,
            seeking_church_denomination_five=form.
            seeking_church_denomination_five.data,
            seeking_church_denomination_six=form.
            seeking_church_denomination_six.data,
            seeking_current_status_one=form.seeking_current_status_one.data,
            seeking_current_status_two=form.seeking_current_status_two.data,
            seeking_current_status_three=form.seeking_current_status_three.
            data,
            seeking_drinking_status_one=form.seeking_drinking_status_one.data,
            seeking_drinking_status_two=form.seeking_drinking_status_two.data,
            seeking_smoking_status_one=form.seeking_smoking_status_one.data,
            seeking_smoking_status_two=form.seeking_smoking_status_two.data,
            seeking_education_level_one=form.seeking_education_level_one.data,
            seeking_education_level_two=form.seeking_education_level_two.data,
            seeking_education_level_three=form.seeking_education_level_three.
            data,
            seeking_education_level_four=form.seeking_education_level_four.
            data,
            seeking_education_level_five=form.seeking_education_level_five.
            data,
            seeking_education_level_six=form.seeking_education_level_six.data,
            seeking_education_level_seven=form.seeking_education_level_seven.
            data,
            seeking_education_level_eight=form.seeking_education_level_eight.
            data,
            seeking_education_level_nine=form.seeking_education_level_nine.
            data,
            seeking_has_children_one=form.seeking_has_children_one.data,
            seeking_has_children_two=form.seeking_has_children_two.data,
            seeking_has_children_three=form.seeking_has_children_three.data,
            seeking_want_children_one=form.seeking_want_children_one.data,
            seeking_want_children_two=form.seeking_want_children_two.data,
            seeking_want_children_three=form.seeking_want_children_three.data,
            seeking_open_for_relocation=form.seeking_open_for_relocation.data)
        db.session.add(seeking)
        db.session.commit()
        flash(
            'You have successfully added details on what you are looking for',
            'success')
        return redirect(
            url_for('seeking.added_preference', id=id, username=username))
    return render_template('seeking/add_preference.html',
                           form=form,
                           data=data,
                           id=id)


# Edit Preference
@seeking.route('/<int:id>/<username>/edit', methods=['POST', 'GET'])
@login_required
def edit(id, username):
    """Edits a range of user seeking requirements"""
    data = Seeking.query.filter_by(user_id=id).first()
    if data is None:
        return redirect(
            url_for('seeking.add_preference', id=id, username=username))
    form = SeekingForm(obj=data)
    if form.validate_on_submit():

        data.seeking_partner = form.seeking_partner.data
        data.seeking_from_height = form.seeking_from_height.data
        data.seeking_to_height = form.seeking_to_height.data
        data.seeking_sex = form.seeking_sex.data

        data.seeking_from_age = form.seeking_from_age.data
        data.seeking_to_age = form.seeking_to_age.data

        data.seeking_country_one = form.seeking_country_one.data
        data.seeking_country_two = form.seeking_country_two.data
        data.seeking_country_three = form.seeking_country_three.data
        data.seeking_country_four = form.seeking_country_four.data
        data.seeking_country_five = form.seeking_country_five.data
        data.seeking_country_six = form.seeking_country_six.data
        data.seeking_country_seven = form.seeking_country_seven.data
        data.seeking_country_eight = form.seeking_country_eight.data

        data.seeking_religion_one = form.seeking_religion_one.data
        data.seeking_religion_two = form.seeking_religion_two.data
        data.seeking_religion_three = form.seeking_religion_three.data

        data.seeking_ethnicity_one = form.seeking_ethnicity_one.data
        data.seeking_ethnicity_two = form.seeking_ethnicity_two.data
        data.seeking_ethnicity_three = form.seeking_ethnicity_three.data
        data.seeking_ethnicity_four = form.seeking_ethnicity_four.data
        data.seeking_ethnicity_five = form.seeking_ethnicity_five.data

        data.seeking_marital_type_one = form.seeking_marital_type_one.data

        data.seeking_body_type_one = form.seeking_body_type_one.data
        data.seeking_body_type_two = form.seeking_body_type_two.data
        data.seeking_body_type_three = form.seeking_body_type_three.data
        data.seeking_body_type_four = form.seeking_body_type_four.data

        data.seeking_church_denomination_one = form.seeking_church_denomination_one.data
        data.seeking_church_denomination_two = form.seeking_church_denomination_two.data
        data.seeking_church_denomination_three = form.seeking_church_denomination_three.data
        data.seeking_church_denomination_four = form.seeking_church_denomination_four.data
        data.seeking_church_denomination_five = form.seeking_church_denomination_five.data
        data.seeking_church_denomination_six = form.seeking_church_denomination_six.data

        data.seeking_current_status_one = form.seeking_current_status_one.data
        data.seeking_current_status_two = form.seeking_current_status_two.data
        data.seeking_current_status_three = form.seeking_current_status_three.data

        data.seeking_drinking_status_one = form.seeking_drinking_status_one.data
        data.seeking_drinking_status_two = form.seeking_drinking_status_two.data

        data.seeking_smoking_status_one = form.seeking_smoking_status_one.data
        data.seeking_smoking_status_two = form.seeking_smoking_status_two.data

        data.seeking_education_level_one = form.seeking_education_level_one.data
        data.seeking_education_level_two = form.seeking_education_level_two.data
        data.seeking_education_level_three = form.seeking_education_level_three.data
        data.seeking_education_level_four = form.seeking_education_level_four.data
        data.seeking_education_level_five = form.seeking_education_level_five.data
        data.seeking_education_level_six = form.seeking_education_level_six.data
        data.seeking_education_level_seven = form.seeking_education_level_seven.data
        data.seeking_education_level_eight = form.seeking_education_level_eight.data
        data.seeking_education_level_nine = form.seeking_education_level_nine.data

        data.seeking_has_children_one = form.seeking_has_children_one.data
        data.seeking_has_children_two = form.seeking_has_children_two.data
        data.seeking_has_children_three = form.seeking_has_children_three.data

        data.seeking_want_children_one = form.seeking_want_children_one.data
        data.seeking_want_children_two = form.seeking_want_children_two.data
        data.seeking_want_children_three = form.seeking_want_children_three.data

        data.seeking_open_for_relocation = form.seeking_open_for_relocation.data

        db.session.add(data)
        db.session.commit()
        flash("Edited Successfully.", "success")
        return redirect(
            url_for('seeking.added_preference', id=id, username=username))
    else:
        flash('ERROR! Preference was not edited.', 'error')
    return render_template('seeking/add_preference.html',
                           form=form,
                           id=id,
                           username=username)


@seeking.route('/<int:id>/<username>/_delete', methods=['GET', 'POST'])
@login_required
def delete(id, username):
    """Delete the preference added """
    if current_user.id != id and current_user.username != username:
        flash("You cannot delete any user's preference.", "warning")
        return redirect(
            url_for('seeking.added_preference', id=id, username=username))
    if current_user.id != id:
        flash("You cannot delete any user's preference.", "warning")
        return redirect(
            url_for('seeking.added_preference', id=id, username=username))

    if current_user.username != username:
        flash("You cannot delete any user's preference.", "warning")
        return redirect(
            url_for('seeking.added_preference', id=id, username=username))

    data = Seeking.query.filter_by(id=id).first()
    db.session.commit()
    db.session.delete(data)
    flash('Successfully deleted ', 'success')
    if data is None:
        return redirect(
            url_for('seeking.add_preference', id=id, username=username))
    return redirect(
        url_for('seeking.added_preference', id=id, username=username))
