from datetime import date

from flask import url_for
from sqlalchemy.orm import backref

from .. import db
from .user import *  # noqa


class EventAttendee(db.Model):
    __tablename__ = 'event_attendees'
    id = db.Column(db.Integer, primary_key=True)
    attendee_id = db.Column(db.Integer,
                            db.ForeignKey('attendees.id', ondelete="CASCADE"))
    event_id = db.Column(db.Integer,
                         db.ForeignKey('events.id', ondelete="CASCADE"))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime,
                           default=db.func.now(),
                           onupdate=db.func.now())


#@whooshee.register_model('event_title', 'event_state', 'event_country')
class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    image_filename = db.Column(db.String, default=None, nullable=True)
    pub_date = db.Column(db.DateTime, default=date.today(), nullable=False)
    start_date = db.Column(db.String, default='now', nullable=False)
    end_date = db.Column(db.String, default='now', nullable=False)
    event_title = db.Column(db.String(255))
    event_city = db.Column(db.String(255))
    online_meeting_link = db.Column(db.String(255))
    event_state = db.Column(db.String(255))
    event_country = db.Column(db.String(255))
    event_type = db.Column(db.String(255))
    free_or_paid = db.Column(db.String(255))
    amount = db.Column(db.String(255))
    street_address = db.Column(db.String(255))
    post_code = db.Column(db.String(255))
    description = db.Column(db.Text)
    creator_id = db.Column(db.Integer,
                           db.ForeignKey('users.id', ondelete="CASCADE"),
                           nullable=False)
    attendees = db.relationship("Attendee",
                                secondary='event_attendees',
                                backref=backref("events", cascade='all'),
                                primaryjoin='Event.id==Attendee.event_id',
                                cascade='all,delete')
    creator = db.relationship("User")
    created_at = db.Column(db.DateTime, default=date.today())
    updated_at = db.Column(db.DateTime,
                           default=date.today(),
                           onupdate=date.today())

    @property
    def user_name(self):
        return User.get(self.organisation_id).user_name

    def get_photo(self):
        if self.image_filename:
            return url_for('_uploads.uploaded_file',
                           setname='images',
                           filename=self.image_filename,
                           _external=True)
        else:
            return self.user.get_photo()

    def __repr__(self):
        return u'<{self.__class__.__name__}: {self.id}>'.format(self=self)


class Attendee(db.Model):
    __tablename__ = 'attendees'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer,
                         db.ForeignKey('events.id', ondelete="CASCADE"),
                         nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id', ondelete="CASCADE"),
                        nullable=False)
    event = db.relationship('Event', cascade='all, delete')
    users = db.relationship('User',
                            order_by=User.id,
                            backref="attendees",
                            cascade="all")
    created_at = db.Column(db.DateTime, default=date.today())
    updated_at = db.Column(db.DateTime,
                           default=date.today(),
                           onupdate=date.today())
