from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import ValidationError
from wtforms.fields import (BooleanField, DateField, EmailField, FileField,
                            FloatField, IntegerField, MultipleFileField,
                            PasswordField, SelectField, StringField,
                            SubmitField, TextAreaField)
from wtforms.validators import (DataRequired, Email, EqualTo, InputRequired,
                                Length)
from wtforms_alchemy import ModelForm, Unique, model_form_factory
from wtforms_alchemy.fields import QuerySelectField, QuerySelectMultipleField

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
