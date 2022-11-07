import os
from datetime import date, datetime, timedelta

from flask import url_for

from .. import db


class ContactMessage(db.Model):
    __tablename__ = 'contact_messages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    read = db.Column(db.Boolean, default=False)
    spam = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id', ondelete="CASCADE"),
                        nullable=True)
    name = db.Column(db.String(), default=None, nullable=True)
    email = db.Column(db.String(64), default=None, nullable=True)
    text = db.Column(db.Text)
    user = db.relationship("User")
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime,
                           default=db.func.now(),
                           onupdate=db.func.now())


def contact_messages_serializer(contact_messages):
    return {
        'id': contact_messages.id,
        'read': contact_messages.read,
        'name': contact_messages.name,
        'email': contact_messages.email,
        'text': contact_messages.text,
        'created_at': contact_messages.created_at,
    }


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id', ondelete='cascade'))
    recipient_id = db.Column(db.Integer,
                             db.ForeignKey('users.id', ondelete="CASCADE"))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=db.func.now())
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime,
                           default=db.func.now(),
                           onupdate=db.func.now())
    read_at = db.Column(db.DateTime, default=None, nullable=True)

    user = db.relationship('User', primaryjoin="Message.user_id==User.id")

    def __repr__(self):
        return '<Message {}>'.format(self.body)
