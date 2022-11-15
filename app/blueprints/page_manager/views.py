from flask import (Blueprint, flash, redirect, render_template,
                   url_for)
from flask_login import login_required
from app import db
from app.blueprints.page_manager.forms import PageForm
from app.common.decorators import admin_required
from app.models import Page


page_manager = Blueprint('page_manager', __name__)


@page_manager.route('/page/setting')
@login_required
@admin_required
def index():
    return render_template('page_manager/page/index.html')


# Add Page
@page_manager.route('/page/setting/added', methods=['POST', 'GET'])
@login_required
@admin_required
def added_page():
    """View added Page setting."""
    data = Page.query.all()
    if data is None:
        return redirect(url_for('page_manager.add_page'))
    return render_template('page_manager/page/added_page.html', data=data)


@page_manager.route('/page/setting/add', methods=['POST', 'GET'])
@login_required
@admin_required
def add_page():
    """Creates a page object"""
    form = PageForm()
    if form.validate_on_submit():
        data = Page(
            name=form.name.data,
            content=form.content.data)
        db.session.add(data)
        db.session.commit()
        flash("Settings Added Successfully.", "success")
        return redirect(url_for('page_manager.added_page'))
    return render_template('page_manager/page/add_page.html', form=form)


# Edit Page
@page_manager.route('/page/<int:id>/edit', methods=['POST', 'GET'])
@login_required
@admin_required
def edit_page(id):
    """Updates an added page"""
    data = Page.query.filter_by(id=id).first()
    form = PageForm(obj=data)
    if form.validate_on_submit():
        data.name = form.name.data
        data.content = form.content.data
        db.session.add(data)
        db.session.commit()
        flash("Link Html Added Successfully.", "success")
        return redirect(url_for('page_manager.added_page'))
    else:
        flash('ERROR! Page was not edited.', 'error')
    return render_template('page_manager/page/add_page.html', form=form)


@page_manager.route('/page/setting/<int:id>/_delete', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_page(id):
    """Delete the page added """
    data = Page.query.filter_by(id=id).first()
    db.session.commit()
    db.session.delete(data)
    flash('Successfully deleted ', 'success')
    if data is None:
        return redirect(url_for('page_manager.add_page'))
    return redirect(url_for('page_manager.added_page'))
