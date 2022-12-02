from flask_wtf import FlaskForm
from wtforms.fields import EmailField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, InputRequired, Length
from wtforms_alchemy import ModelForm, model_form_factory

from app import db
from app.models import *

BaseModelForm = model_form_factory(FlaskForm)


class PublicContactForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    email = EmailField('Email',
                       validators=[InputRequired(),
                                   Length(1, 64),
                                   Email()])
    text = TextAreaField('Message', validators=[InputRequired()])
    submit = SubmitField('Send')


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    email = EmailField('Email',
                       validators=[InputRequired(),
                                   Length(1, 64),
                                   Email()])
    text = TextAreaField('Message', validators=[InputRequired()])
    submit = SubmitField('Send')


class MessageForm(FlaskForm):
    message = StringField(('Message'),
                          validators=[DataRequired(),
                                      Length(min=1, max=2500)])
    submit = SubmitField(('Submit'))
