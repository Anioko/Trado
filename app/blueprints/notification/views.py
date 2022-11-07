from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    jsonify
)
from flask_login import current_user, login_required
from app.common.flask_rq import get_queue

from flask_ckeditor import upload_success
from flask_sqlalchemy.pagination import Pagination
from sqlalchemy import desc, func

from app import db
# from app.page_manager.forms import (
# ChangeAccountTypeForm,
# ChangeUserEmailForm,
# InviteUserForm,
# NewUserForm,
# )
from app.models import *
from app.blueprints.notification.forms import *

notification = Blueprint('notification', __name__)


@notification.route('/read/<notification_id>')
@login_required
def read_notification(notification_id):
    notification = current_user.notifications.filter_by(
        id=notification_id).first_or_404()
    notification.read = True
    db.session.add(notification)
    db.session.commit()
    if 'unread_message' in notification.name:
        user = User.query.filter_by(id=notification.related_id).first_or_404()
        link = url_for('notification.send_message',
                       recipient=user.id, full_name=user.full_name)

    return redirect(link)


@notification.route('/count')
@login_required
def notifications_count():
    notifications = Notification.query.filter_by(
        read=False).filter_by(user_id=current_user.id).count()
    messages = current_user.new_messages()

    return jsonify({
        'status': 1,
        'notifications': notifications,
        'messages': messages
    })


@notification.route('/')
@login_required
def notifications():
    users = User.query.order_by(User.username).all()
    notifications = current_user.notifications.all()
    parsed_notifications = []
    for notification in notifications:
        parsed_notifications.append(notification.parsed())
    parsed_notifications = sorted(
        parsed_notifications, key=lambda i: i['time'])
    parsed_notifications.reverse()
    parsed_notifications = parsed_notifications[0:15]
    return render_template('notification/notifications.html', users=users,
                           notifications=parsed_notifications)


@notification.route('/more/<int:count>')
@login_required
def more_notifications(count):
    # follow_lists = User.query.filter(User.id != current_user.id).order_by(func.random()).limit(10).all()
    # jobs = Job.query.filter(Job.organisation != None).filter(Job.end_date >= datetime.now()).order_by(Job.pub_date.asc()).all()
    # users = User.query.order_by(User.full_name).all()
    notifications = current_user.notifications.all()
    print(len(notifications))
    parsed_notifications = []
    for notification in notifications:
        parsed_notifications.append(notification.parsed())
    parsed_notifications = sorted(
        parsed_notifications, key=lambda i: i['time'])
    parsed_notifications.reverse()
    if count == 0:
        parsed_notifications = parsed_notifications[0:15]
    elif count >= len(parsed_notifications):
        return "<br><br><h2>No more Notifications</h2>"
    else:
        parsed_notifications = parsed_notifications[count:count + 15]
    return render_template('notification/more_notifications.html', notifications=parsed_notifications)


@notification.route('/notification_test')
@login_required
def notification_test():
    n = Notification.query.get(379)
    related = User.query.get(32)
    extraextra = Answer.query.get(25)
    return render_template('account/email/notification.html', user=current_user, link="http://www.google.com",
                           notification=n, related=related,
                           extraextra=extraextra)
