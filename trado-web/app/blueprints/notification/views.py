from flask import (Blueprint, jsonify, redirect, render_template, url_for)
from flask_login import current_user, login_required
from app import db
from app.models import User, Notification

notification = Blueprint('notification', __name__)


@notification.route('/read/<notification_id>')
@login_required
def read_notification(notification_id):
    """Returns a notification object while also setting read value"""
    notification = current_user.notifications.filter_by(
        id=notification_id).first_or_404()
    notification.read = True
    db.session.add(notification)
    db.session.commit()
    if 'unread_message' in notification.name:
        user = User.query.filter_by(id=notification.related_id).first_or_404()
        link = url_for('notification.send_message',
                       recipient=user.id,
                       full_name=user.full_name)

    return redirect(link)


@notification.route('/count')
@login_required
def notifications_count():
    """Returns a number representing user notifications"""
    notifications = Notification.query.filter_by(read=False).filter_by(
        user_id=current_user.id).count()
    messages = current_user.new_messages()

    return jsonify({
        'status': 1,
        'notifications': notifications,
        'messages': messages
    })


@notification.route('/')
@login_required
def notifications():
    """Returns a list of user notifications"""
    users = User.query.order_by(User.username).all()
    notifications = current_user.notifications.all()
    parsed_notifications = []
    for notification in notifications:
        parsed_notifications.append(notification.parsed())
    parsed_notifications = sorted(parsed_notifications,
                                  key=lambda i: i['time'])
    parsed_notifications.reverse()
    parsed_notifications = parsed_notifications[0:15]
    return render_template('notification/notifications.html',
                           users=users,
                           notifications=parsed_notifications)


@notification.route('/more/<int:count>')
@login_required
def more_notifications(count):
    """Allows a callbck to fetch remaining notifications"""
    notifications = current_user.notifications.all()
    parsed_notifications = []
    for notification in notifications:
        parsed_notifications.append(notification.parsed())
    parsed_notifications = sorted(parsed_notifications,
                                  key=lambda i: i['time'])
    parsed_notifications.reverse()
    if count == 0:
        parsed_notifications = parsed_notifications[0:15]
    elif count >= len(parsed_notifications):
        return "<br><br><h2>No more Notifications</h2>"
    else:
        parsed_notifications = parsed_notifications[count:count + 15]
    return render_template('notification/more_notifications.html',
                           notifications=parsed_notifications)
