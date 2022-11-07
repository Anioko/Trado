import os

from flask import url_for

from app import whooshee

from .. import db


@whooshee.register_model(
    'seeking_partner', 'seeking_from_height', 'seeking_to_height',
    'seeking_sex', 'seeking_from_age', 'seeking_to_age'
    'seeking_church_denomination_one', 'seeking_church_denomination_two',
    'seeking_church_denomination_three', 'seeking_church_denomination_four',
    'seeking_church_denomination_five', 'seeking_church_denomination_six',
    'seeking_open_for_relocation')
class Seeking(db.Model):
    __tablename__ = 'seeking'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates="seeking")
    seeking_partner = db.Column(db.String(80), nullable=True)
    seeking_from_height = db.Column(db.String(80), nullable=True)
    seeking_to_height = db.Column(db.String(80), nullable=True)
    seeking_sex = db.Column(db.String(80), nullable=True)
    seeking_from_age = db.Column(db.Integer, nullable=True)
    seeking_to_age = db.Column(db.Integer, nullable=True)
    seeking_sex = db.Column(db.String(80), nullable=True)

    seeking_education_level_one = db.Column(db.String(80), nullable=True)
    seeking_education_level_two = db.Column(db.String(80), nullable=True)
    seeking_education_level_three = db.Column(db.String(80), nullable=True)
    seeking_education_level_four = db.Column(db.String(80), nullable=True)
    seeking_education_level_five = db.Column(db.String(80), nullable=True)
    seeking_education_level_six = db.Column(db.String(80), nullable=True)
    seeking_education_level_seven = db.Column(db.String(80), nullable=True)
    seeking_education_level_eight = db.Column(db.String(80), nullable=True)

    seeking_church_denomination_one = db.Column(db.String(80), nullable=True)
    seeking_church_denomination_two = db.Column(db.String(80), nullable=True)
    seeking_church_denomination_three = db.Column(db.String(80), nullable=True)
    seeking_church_denomination_four = db.Column(db.String(80), nullable=True)
    seeking_church_denomination_five = db.Column(db.String(80), nullable=True)
    seeking_church_denomination_six = db.Column(db.String(80), nullable=True)

    seeking_country_one = db.Column(db.String(80), nullable=True)
    seeking_country_two = db.Column(db.String(80), nullable=True)
    seeking_country_three = db.Column(db.String(80), nullable=True)
    seeking_country_four = db.Column(db.String(80), nullable=True)
    seeking_country_five = db.Column(db.String(80), nullable=True)
    seeking_country_six = db.Column(db.String(80), nullable=True)
    seeking_country_seven = db.Column(db.String(80), nullable=True)
    seeking_country_eight = db.Column(db.String(80), nullable=True)

    seeking_religion_one = db.Column(db.String(80), nullable=True)
    seeking_religion_two = db.Column(db.String(80), nullable=True)
    seeking_religion_three = db.Column(db.String(80), nullable=True)

    seeking_ethnicity_one = db.Column(db.String(80), nullable=True)
    seeking_ethnicity_two = db.Column(db.String(80), nullable=True)
    seeking_ethnicity_three = db.Column(db.String(80), nullable=True)
    seeking_ethnicity_four = db.Column(db.String(80), nullable=True)
    seeking_ethnicity_five = db.Column(db.String(80), nullable=True)

    seeking_marital_type_one = db.Column(db.String(80), nullable=True)
    seeking_marital_type_two = db.Column(db.String(80), nullable=True)
    seeking_marital_type_three = db.Column(db.String(80), nullable=True)

    seeking_body_type_one = db.Column(db.String(80), nullable=True)
    seeking_body_type_two = db.Column(db.String(80), nullable=True)
    seeking_body_type_three = db.Column(db.String(80), nullable=True)
    seeking_body_type_four = db.Column(db.String(80), nullable=True)

    seeking_education_level_one = db.Column(db.String(80), nullable=True)
    seeking_education_level_two = db.Column(db.String(80), nullable=True)
    seeking_education_level_three = db.Column(db.String(80), nullable=True)
    seeking_education_level_four = db.Column(db.String(80), nullable=True)
    seeking_education_level_five = db.Column(db.String(80), nullable=True)
    seeking_education_level_six = db.Column(db.String(80), nullable=True)

    seeking_current_status_one = db.Column(db.String(80), nullable=True)
    seeking_current_status_two = db.Column(db.String(80), nullable=True)
    seeking_current_status_three = db.Column(db.String(80), nullable=True)

    seeking_drinking_status_one = db.Column(db.String(80), nullable=True)
    seeking_drinking_status_two = db.Column(db.String(80), nullable=True)

    seeking_smoking_status_one = db.Column(db.String(80), nullable=True)
    seeking_smoking_status_two = db.Column(db.String(80), nullable=True)

    seeking_education_level_one = db.Column(db.String(80), nullable=True)
    seeking_education_level_two = db.Column(db.String(80), nullable=True)
    seeking_education_level_three = db.Column(db.String(80), nullable=True)
    seeking_education_level_four = db.Column(db.String(80), nullable=True)
    seeking_education_level_five = db.Column(db.String(80), nullable=True)
    seeking_education_level_six = db.Column(db.String(80), nullable=True)
    seeking_education_level_seven = db.Column(db.String(80), nullable=True)
    seeking_education_level_eight = db.Column(db.String(80), nullable=True)
    seeking_education_level_nine = db.Column(db.String(80), nullable=True)

    seeking_has_children_one = db.Column(db.String(80), nullable=True)
    seeking_has_children_two = db.Column(db.String(80), nullable=True)
    seeking_has_children_three = db.Column(db.String(80), nullable=True)

    seeking_want_children_one = db.Column(db.String(80), nullable=True)
    seeking_want_children_two = db.Column(db.String(80), nullable=True)
    seeking_want_children_three = db.Column(db.String(80), nullable=True)

    seeking_open_for_relocation = db.Column(db.String(80), nullable=True)

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id', ondelete="CASCADE"),
                        nullable=True)
