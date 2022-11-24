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
#from app.admin.forms import (
    #ChangeAccountTypeForm,
    #ChangeUserEmailForm,
    #InviteUserForm,
    #NewUserForm,
#)
from app.decorators import admin_required
from app.email import send_email
from app.models import *
from app.blueprints.profile.forms import *

profile = Blueprint('profile', __name__)


@profile.route('/settings')
@login_required
def settings():
    return render_template('profile/settings.html')

####################Content Management System Start #################




@profile.route('/<int:user_id>/<username>/info')
@login_required
#@admin_required
def view(user_id, username):
    """View a user's profile."""
    user = User.query.filter_by(id=user_id, username=username).first()
    if user is None:
        abort(404)
    profile_picture = Photo.query.filter_by(user_id=user.id, profile_picture=True).first()
    photo_data = Photo.query.filter_by(user_id=user.id).all()
    #preferences_data = Seeking.query.filter_by(user_id=current_user.id).first()
    preferences_data = Seeking.query.filter_by(user_id=user.id).first()    
    return render_template('socialite/index.html',  user=user, photo_data=photo_data, preferences_data=preferences_data,
                           profile_picture=profile_picture)



@profile.route('/list/', defaults={'page': 1})
@profile.route('/list/page/<int:page>', methods=['GET'])
def members(page):
    paginated = User.query.filter(User.id != current_user.id).order_by(User.id.desc()).paginate(page, per_page=25)
    return render_template('profile/members.html', paginated=paginated)
