from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.fields import (
    PasswordField,
    StringField,
    SubmitField,
    FloatField,
    MultipleFileField,
    FileField,
    SelectField,
    DateField, 
    TextAreaField,
    IntegerField,
    BooleanField

)
from wtforms.fields.html5 import EmailField
from wtforms.validators import (
    Email,
    EqualTo,
    InputRequired,
    Length,
    DataRequired
)

from app import db
from app.models import *
from wtforms_alchemy import Unique, ModelForm, model_form_factory

BaseModelForm = model_form_factory(FlaskForm)

class PublicContactForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    email = EmailField('Email', validators=[InputRequired(), Length(1, 64), Email()])
    text = TextAreaField('Message', validators=[InputRequired()])
    submit = SubmitField('Send')



class ContactForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    email = EmailField('Email', validators=[InputRequired(), Length(1, 64), Email()])
    text = TextAreaField('Message', validators=[InputRequired()])
    submit = SubmitField('Send')

