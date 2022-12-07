import os
from flask import url_for
from .. import db
from app import whooshee


class Seeking(db.Model):
    __tablename__ = 'seeking'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates="seeking")
    seeking_partner = db.Column(db.String(80), nullable=True)
    seeking_from_height = db.Column(db.String(80), nullable=True)
    seeking_to_height = db.Column(db.String(80), nullable=True)
    seeking_from_age = db.Column(db.Integer, nullable=True)
    seeking_to_age = db.Column(db.Integer, nullable=True)
    seeking_education_level = db.Column(db.String(80), nullable=True)
    seeking_country = db.Column(db.String(80), nullable=True)
    seeking_religion = db.Column(db.String(80), nullable=True)
    seeking_ethnicity = db.Column(db.String(80), nullable=True)
    seeking_marital_type = db.Column(db.String(80), nullable=True)
    seeking_body_type = db.Column(db.String(80), nullable=True)
    seeking_drinking_status = db.Column(db.String(80), nullable=True)
    seeking_smoking_status = db.Column(db.String(80), nullable=True)
    seeking_has_children = db.Column(db.String(80), nullable=True)
    seeking_want_children = db.Column(db.String(80), nullable=True)    
    seeking_open_for_relocation = db.Column(db.String(80), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=True)
    