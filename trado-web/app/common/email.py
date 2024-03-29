import os

from flask import render_template
from flask_mail import Message

from app import create_app, mail
from .celery import celery


@celery.task(name='send_email')
def send_email(recipient, subject, template, **kwargs):
    app = create_app(os.getenv('FLASK_CONFIG') or 'default')
    with app.app_context():
        msg = Message(app.config['EMAIL_SUBJECT_PREFIX'] + ' ' + subject,
                      sender=app.config['MAIL_DEFAULT_SENDER'],
                      recipients=[recipient])
        msg.body = template
        msg.html = template
        #msg.body = render_template(template + '.txt', **kwargs)
        #msg.html = render_template(template + '.html', **kwargs)
        mail.send(msg)
