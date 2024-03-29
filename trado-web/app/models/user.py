import json
from datetime import datetime, timedelta, timezone
from enum import Enum

import jwt
import socketio
from flask import current_app, url_for
from flask_jwt_extended import create_access_token
from flask_login import AnonymousUserMixin, UserMixin, current_user
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from sqlalchemy import and_, or_
from werkzeug.security import check_password_hash, generate_password_hash

from app import whooshee
from app.common.flask_rq import get_queue
from app.common.utils import jsonify_object

from .. import db, login_manager
from .messaging_manager import Message  # noqa
from .notification import Notification


class Permission(str, Enum):
    GENERAL = "General"
    ADMINISTER = "Administer"


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    index = db.Column(db.String(64))
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.String, default=Permission.GENERAL, index=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.GENERAL, 'main', True),
            'Administrator': (
                Permission.ADMINISTER,
                'admin',
                False  # grants all permissions
            )
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.index = roles[r][1]
            role.default = roles[r][2]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role \'%s\'>' % self.name


@whooshee.register_model('username', 'marital_type', 'age', 'country',
                         'religion', 'ethnicity', 'state', 'education_level')
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    confirmed = db.Column(db.Boolean, default=False)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    height = db.Column(db.String(64), index=True)
    sex = db.Column(db.String(64), index=True)
    seeking_gender = db.Column(db.String(10), index=True)
    age = db.Column(db.String(64), index=True)
    state = db.Column(db.String(64), index=True)
    country = db.Column(db.String(64), index=True)
    religion = db.Column(db.String(64), index=True)
    ethnicity = db.Column(db.String(64), index=True)
    marital_type = db.Column(db.String(64), index=True)
    body_type = db.Column(db.String(64), index=True)
    church_denomination = db.Column(db.String(64), index=True)
    #about = db.Column(db.Text)
    current_status = db.Column(db.String(64), index=True)
    drinking_status = db.Column(db.String(64), index=True)
    smoking_status = db.Column(db.String(64), index=True)
    education_level = db.Column(db.String(64), index=True)
    has_children = db.Column(db.String(64), index=True)
    want_children = db.Column(db.String(64), index=True)
    open_for_relocation = db.Column(db.String(64), index=True)
    is_public = db.Column(db.Boolean, default=False, index=True)
    seeking = db.relationship('Seeking',
                              back_populates='user',
                              lazy='dynamic',
                              cascade='all')
    photos = db.relationship('Photo', backref='user', lazy='dynamic')
    messages_received = db.relationship('Message',
                                        foreign_keys='Message.recipient_id',
                                        backref='recipient',
                                        lazy='dynamic')
    notifications = db.relationship('Notification',
                                    backref='user',
                                    lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['ADMIN_EMAIL']:
                self.role = Role.query.filter_by(
                    permissions=Permission.ADMINISTER).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def can(self, permissions):
        return self.role is not None and \
            self.role.permissions == permissions

    def is_admin(self):
        return self.can(Permission.ADMINISTER)

    @property
    def password(self):
        raise AttributeError('`password` is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=604800):
        """Generate a confirmation token to email a new user."""
        reset_token = jwt.encode(
            {
                "confirm":
                self.id,
                "exp":
                datetime.now(tz=timezone.utc) + timedelta(seconds=expiration)
            },
            current_app.config['SECRET_KEY'],
            algorithm="HS256")
        return reset_token

    def generate_email_change_token(self, new_email, expiration=3600):
        """Generate an email change token to email an existing user."""
        reset_token = jwt.encode(
            {
                'change_email':
                self.id,
                'new_email':
                new_email,
                "exp":
                datetime.now(tz=timezone.utc) + timedelta(seconds=expiration)
            },
            current_app.config['SECRET_KEY'],
            algorithm="HS256")
        return reset_token

    def generate_password_reset_token(self, expiration=3600):
        """
        Generate a password reset change token to email to an existing user.
        """
        reset_token = jwt.encode(
            {
                "reset":
                self.id,
                "exp":
                datetime.now(tz=timezone.utc) + timedelta(seconds=expiration)
            },
            current_app.config['SECRET_KEY'],
            algorithm="HS256")
        return reset_token

    def confirm_account(self, token, expiration=604800):
        """Verify that the provided token is for this user's id."""
        try:
            data = jwt.decode(token,
                              current_app.config['SECRET_KEY'],
                              leeway=timedelta(seconds=expiration),
                              algorithms=["HS256"])
        except (InvalidTokenError, ExpiredSignatureError):
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    def change_email(self, token, expiration=3600):
        """Verify the new email for this user."""
        try:
            data = jwt.decode(token,
                              current_app.config['SECRET_KEY'],
                              leeway=timedelta(seconds=expiration),
                              algorithms=["HS256"])
        except (InvalidTokenError, ExpiredSignatureError):
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        db.session.commit()
        return True

    def reset_password(self, token, new_password, expiration=3600):
        """Verify the new password for this user."""
        try:
            data = jwt.decode(token,
                              current_app.config['SECRET_KEY'],
                              leeway=timedelta(seconds=expiration),
                              algorithms=["HS256"])
        except (InvalidTokenError, ExpiredSignatureError):
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        db.session.commit()
        return True

    @staticmethod
    def generate_fake(count=100, **kwargs):
        """Generate a number of fake users for testing."""
        from random import choice, seed

        from faker import Faker
        from sqlalchemy.exc import IntegrityError

        fake = Faker()
        roles = Role.query.all()

        seed()
        for i in range(count):
            u = User(first_name=fake.first_name(),
                     username=fake.first_name(),
                     country=fake.country(),
                     last_name=fake.last_name(),
                     email=fake.email(),
                     password='password',
                     confirmed=True,
                     role=choice(roles),
                     **kwargs)
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def new_messages(self, user_id=None):
        if user_id is None:
            return Message.query.filter_by(recipient=self).filter(
                Message.read_at == None).distinct('user_id').count()
        else:
            return Message.query.filter_by(recipient=self).filter(
                Message.read_at == None).filter(
                    Message.user_id == user_id).count()

    def last_message(self, user_id):
        message = Message.query.order_by(Message.timestamp.desc()). \
            filter(or_(and_(Message.recipient_id == user_id, Message.user_id == self.id),
                       and_(Message.recipient_id == self.id, Message.user_id == user_id))).first()
        return message

    def history(self, user_id, unread=False):
        messages = Message.query.order_by(Message.timestamp.asc()). \
            filter(or_(and_(Message.recipient_id == user_id, Message.user_id == self.id),
                       and_(Message.recipient_id == self.id, Message.user_id == user_id))).all()
        return messages

    def add_notification(self, name, data, related_id=0, permanent=False):
        from app.common.email import send_email

        if not permanent:
            self.notifications.filter_by(name=name).delete()
        n = Notification(name=name,
                         payload_json=json.dumps(data),
                         user=self,
                         related_id=related_id)
        db.session.add(n)
        db.session.commit()
        n = Notification.query.get(n.id)
        kwargs = data
        kwargs['related'] = related_id
        get_queue().enqueue(
            send_email,
            recipient=self.email,
            subject='You Have a new notification on TraditionalMarriage',
            template='account/email/notification',
            user=self.id,
            link=url_for('main.notifications', _external=True),
            notification=n.id,
            **kwargs)
        if not current_app.config['DEBUG']:
            ws_url = "https://www.traditionalmarriage.org"
            path = 'sockets/socket.io'
        else:
            get_queue().empty()
            ws_url = "http://localhost:3000"
            path = "socket.io"
        sio = socketio.Client()
        sio.connect(ws_url + "?token={}".format(
            create_access_token(identity=current_user.email)),
            socketio_path=path)
        data = n.parsed()
        u = jsonify_object(data['user'])
        tu = jsonify_object(self)
        data['user'] = {
            key: u[key]
            for key in u.keys()
            & {'first_name', 'id', 'email', 'socket_id'}
        }
        data['touser'] = {
            key: tu[key]
            for key in tu.keys()
            & {'first_name', 'id', 'email', 'socket_id'}
        }
        sio.emit('new_notification', {'notification': data})
        return n

    def get_photo(self):
        photos = self.photos.all()
        if len(photos) > 0:
            return photos[0].image_url
        else:
            if self.sex == 'Female':
                return "https://1.semantic-ui.com/images/avatar/large/veronika.jpg"
            else:
                return "https://1.semantic-ui.com/images/avatar/large/jenny.jpg"

    def __repr__(self):
        return '<User \'%s\'>' % self.full_name()


class AnonymousUser(AnonymousUserMixin):

    def can(self, _):
        return False

    def is_admin(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
