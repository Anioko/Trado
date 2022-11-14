import os
from time import time

from flask import url_for
from sqlalchemy.orm import backref

from .. import db
from .user import *  # noqa


class Photo(db.Model):
    __tablename__ = "photo"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(User.id,
                                                    ondelete="CASCADE"))
    image = db.Column(db.String(256), nullable=True)
    profile_picture = db.Column(db.Boolean, default=False, index=True)

    @property
    def image_url(self):
        return url_for('_uploads.uploaded_file',
                       setname='images',
                       filename=self.image,
                       external=True)

    @property
    def image_path(self):
        from flask import current_app
        return os.path.join(current_app.config['UPLOADED_IMAGES_DEST'],
                            self.image)
