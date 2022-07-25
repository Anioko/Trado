from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required
from flask_rq import get_queue
from flask_ckeditor import upload_success
from flask_sqlalchemy import Pagination

from app import db
#from app.page_manager.forms import (
    #ChangeAccountTypeForm,
    #ChangeUserEmailForm,
    #InviteUserForm,
    #NewUserForm,
#)
from app.decorators import admin_required
from app.email import send_email
from app.models import *
from app.blueprints.page_manager.forms import *

page_manager = Blueprint('page_manager', __name__)


@page_manager.route('/page/setting')
@login_required
def index():
    return render_template('page_manager/page/index.html')

# Add Page
@page_manager.route('/page/setting/added', methods=['POST', 'GET'])
@login_required
def added_page():
    """View added Page setting."""
    data = Page.query.all()
    if data is None:
        return redirect(url_for('page_manager.add_page'))
    return render_template(
        'page_manager/page/added_page.html', data=data)


@page_manager.route('/page/setting/add', methods=['POST', 'GET'])
@login_required
def add_page():
    form = PageForm()
    if form.validate_on_submit():
        data = Page(
            name = form.name.data,
            #seo_title = form.seo_title.data,
            #seo_description = form.seo_description.data,
            content = form.content.data
            )
        db.session.add(data)
        db.session.commit()
        flash("Settings Added Successfully.", "success")
        return redirect(url_for('page_manager.added_page'))
    return render_template('page_manager/page/add_page.html', form=form)


# Edit Page
@page_manager.route('/page/<int:id>/edit', methods=['POST', 'GET'])
@login_required
def edit_page(id):
    data = Page.query.filter_by(id=id).first()
    form = PageForm(obj=data)
    if form.validate_on_submit():
        data.name=form.name.data
        data.content=form.content.data
        db.session.add(data)
        db.session.commit()
        flash("Link Html Added Successfully.", "success")
        return redirect(url_for('page_manager.added_page'))
    else:
        flash('ERROR! Page was not edited.', 'error')
    return render_template('page_manager/page/add_page.html', form=form)

@page_manager.route('/page/setting/<int:id>/_delete', methods=['GET', 'POST'])
@login_required
def delete_page(id):
    """Delete the page added """
    data = Page.query.filter_by(id=id).first()
    db.session.commit()
    db.session.delete(data)
    flash('Successfully deleted ' , 'success')
    if data is None:
        return redirect(url_for('page_manager.add_page'))
    return redirect(url_for('page_manager.added_page'))


###Add SubPage 
##@page_manager.route('/<page>/<int:page_id>/add_sub_page', methods=['POST', 'GET'])
##@login_required
##def add_sub_page(page_id, page):
##    #page_id = Page.query.filter_by(id=id).first()
##    page=page
##    form = PageForm()
##    if form.validate_on_submit():
##        data = SubPage(
##            name = form.name.data,
##            content = form.content.data,
##            page_id=page_id,
##            main_page_name=page
##            )
##        db.session.add(data)
##        db.session.commit()
##        flash("Settings Added Successfully.", "success")
##        return redirect(url_for('page_manager.added_sub_page', page_id=page_id, page=page))
##    return render_template('page_manager/page/add_sub_page.html', form=form, page=page)
##
##@page_manager.route('/<page>/<int:page_id>/', methods=['POST', 'GET'])
##@login_required
##def added_sub_page(page_id, page):
##    """View added SubPage  setting."""
##    data = SubPage.query.filter_by(page_id=page_id).all()
##    page_data = SubPage.query.filter_by(page_id=page_id).first()
##    if data is None:
##        return redirect(url_for('page_manager.add_sub_page', page_id=page_id))
##    return render_template(
##        'page_manager/page/added_sub_page.html', data=data, page=page, page_id=page_id, page_data = page_data)
##
##
### Edit SubPage
##@page_manager.route('/<main_page_name>/<sub_page>/<int:id>/edit', methods=['POST', 'GET'])
##@login_required
##def edit_sub_page(id, main_page_name, sub_page):
##    data = SubPage.query.filter_by(id=id).first()
##    main_page_id = data.page_id
##    main_page_name = data.main_page_name
##    form = PageForm(obj=data)
##    if form.validate_on_submit():
##        data.name=form.name.data
##        data.content=form.content.data
##        db.session.add(data)
##        db.session.commit()
##        flash("SubPage Added Successfully.", "success")
##        return redirect(url_for('page_manager.added_sub_page', page_id=main_page_id, page=main_page_name))
##            
##    else:
##        flash('ERROR! SubPage was not edited.', 'error')
##    return render_template('page_manager/page/add_sub_page.html', form=form)
##
###Delete only sub page
##@page_manager.route('/<int:id>/_delete', methods=['GET', 'POST'])
##@login_required
##def delete_sub_page(id):
##    """Delete the page attribute added """
##    data = SubPage.query.filter_by(id=id).first()
##    db.session.commit()
##    db.session.delete(data)
##    flash('Successfully deleted ' , 'success')
##    return redirect(url_for('page_manager.added_sub_page', page_id=data.page_id, page=data.page))
