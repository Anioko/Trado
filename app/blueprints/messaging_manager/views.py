import json
from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   url_for)
from flask_login import current_user, login_required
from sqlalchemy import or_
from datetime import datetime
from app import db
from app.blueprints.messaging_manager.forms import MessageForm
from app.models import User, ContactMessage, Message

messaging_manager = Blueprint('messaging_manager', __name__)


@messaging_manager.route('/<recipient>/<username>', methods=['GET', 'POST'])
@login_required
@login_required
def send_message(recipient, username):
    user = User.query.filter(User.id != current_user.id).filter_by(
        id=recipient).first_or_404()
    for message in current_user.history(user.id):
        if message.recipient_id == current_user.id:
            message.read_at = db.func.now()
        db.session.add(message)
    db.session.commit()
    form = MessageForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            msg = Message(user_id=current_user.id,
                          recipient=user,
                          body=form.message.data)
            db.session.add(msg)
            db.session.commit()
            user.add_notification('unread_message_count', user.new_messages())
            flash('Your message has been sent.')
            return redirect(
                url_for('main.send_message',
                        recipient=user.id,
                        username=user.username))
    return render_template('messaging_manager/send_messages.html',
                           title='Send Message',
                           form=form,
                           recipient=user,
                           current_user=current_user)


@messaging_manager.route('/', defaults={'page': 1}, methods=['GET'])
@messaging_manager.route('/<int:page>', methods=['GET'])
@login_required
def conversations(page):
    current_user.last_message_read_time = datetime.utcnow()
    db.session.commit()

    messages = current_user.messages_received.order_by(
        Message.timestamp.desc()).paginate(page=page, per_page=10)
    conversations = Message.query.filter(
        or_(Message.user_id == current_user.id,
            Message.recipient_id == current_user.id)).all()
    user_ids = [conversation.user_id for conversation in conversations] + [
        conversation.recipient_id for conversation in conversations
    ]
    user_ids = list(set(user_ids))

    if current_user.id in user_ids:
        user_ids.remove(current_user.id)
    users = User.query.filter(User.id.in_(user_ids)).paginate(page=page,
                                                              per_page=20)

    return render_template('messaging_manager/messages.html',
                           messages=messages.items,
                           users=users)


@messaging_manager.route('/contact_messages',
                         defaults={
                             'page': 1,
                             'mtype': 'primary'
                         },
                         methods=['GET'])
@messaging_manager.route('/contact_messages/<string:mtype>',
                         defaults={'page': 1},
                         methods=['GET'])
@messaging_manager.route('/contact_messages/<string:mtype>/<int:page>',
                         defaults={'mtype': 'primary'},
                         methods=['GET'])
@login_required
def contact_messages(mtype, page):
    if mtype == 'primary':
        contact_messages_result = ContactMessage.query.filter_by(
            spam=False).order_by(ContactMessage.created_at.desc()).paginate(
                page=page, per_page=100)
    elif mtype == 'spam':
        contact_messages_result = ContactMessage.query.filter(
            (ContactMessage.spam == True)
            | (ContactMessage.spam == None)).order_by(
                ContactMessage.created_at.desc()).paginate(page=page,
                                                           per_page=100)
        print(contact_messages_result.items)
    else:
        abort(404)
    return render_template('messaging_manager/contact_messages/browse.html',
                           contact_messages=contact_messages_result,
                           mtype=mtype)


@messaging_manager.route('/contact_message/<message_id>', methods=['GET'])
@login_required
def view_contact_message(message_id):
    message = ContactMessage.query.filter_by(id=message_id).first_or_404()
    message.read = True
    db.session.commit()
    return render_template('messaging_manager/contact_messages/view.html',
                           contact_message=message)


@messaging_manager.route('/contact_messages/<int:message_id>/_delete',
                         methods=['POST'])
@login_required
def delete_contact_message(message_id):
    message = ContactMessage.query.filter_by(id=message_id).first()
    db.session.delete(message)
    db.session.commit()
    flash('Successfully deleted Message.', 'success')
    return redirect(url_for('messaging_manager.contact_messages'))


@messaging_manager.route('/contact_messages/<int:message_id>/_toggle',
                         methods=['POST'])
@login_required
def toggle_message(message_id):
    message = ContactMessage.query.filter_by(id=message_id).first()
    message.spam = not message.spam
    db.session.commit()
    flash('Successfully toggles Message status.', 'success')
    return redirect(url_for('messaging_manager.contact_messages'))


@messaging_manager.route('/contact_messages/batch_toggle', methods=['POST'])
@login_required
def batch_toggle():
    try:
        ids = json.loads(request.form.get('items'))
    except:
        flash('Something went wrong, pls try again.', 'error')
        return redirect(url_for('messaging_manager.contact_messages'))

    messages = ContactMessage.query.filter(ContactMessage.id.in_(ids)).all()
    print(messages)
    for message in messages:
        message.spam = not message.spam
    db.session.commit()
    flash('Successfully toggles Messages status.', 'success')
    return redirect(url_for('messaging_manager.contact_messages'))


@messaging_manager.route('/contact_messages/batch_delete', methods=['POST'])
@login_required
def batch_delete():
    try:
        ids = json.loads(request.form.get('items'))
    except:
        flash('Something went wrong, pls try again.', 'error')
        return redirect(url_for('messaging_manager.contact_messages'))

    messages = ContactMessage.query.filter(
        ContactMessage.id.in_(ids)).delete(synchronize_session=False)
    # db.session.delete(messages)
    db.session.commit()
    flash('Successfully deleted Messages.', 'success')
    return redirect(url_for('messaging_manager.contact_messages'))
