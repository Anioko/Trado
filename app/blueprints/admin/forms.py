from flask_wtf import FlaskForm
from app.common.flask_uploads import UploadSet, IMAGES
from flask_wtf.file import FileAllowed
from flask_ckeditor import CKEditorField
from wtforms import ValidationError
from wtforms_alchemy import QuerySelectField, QuerySelectMultipleField
from wtforms.fields import PasswordField, StringField, SubmitField, BooleanField, IntegerField, FloatField, \
    MultipleFileField, TextAreaField, SelectField, FileField, EmailField
from wtforms.validators import (
    Email,
    EqualTo,
    InputRequired,
    Length,
)
from wtforms_alchemy import Unique, ModelForm, model_form_factory
from app import db
from app.models import Role, User, BlogCategory, BlogTag, BlogNewsLetter

images = UploadSet('images', IMAGES)
BaseModelForm = model_form_factory(FlaskForm)


class ChangeUserEmailForm(FlaskForm):
    email = EmailField(
        'New email', validators=[InputRequired(),
                                 Length(1, 64),
                                 Email()])
    submit = SubmitField('Update email')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class ChangeAccountTypeForm(FlaskForm):
    role = QuerySelectField(
        'New account type',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(Role).order_by('permissions'))
    submit = SubmitField('Update role')

class ConfirmAccountForm(FlaskForm):
    confirmed = BooleanField('True: Tick this checkbox to confirm the users account manually',
                             validators=[InputRequired()])
    submit = SubmitField('Confirm')


class InviteUserForm(FlaskForm):
    role = QuerySelectField(
        'Account type',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(Role).order_by('permissions'))
    first_name = StringField(
        'First name', validators=[InputRequired(),
                                  Length(1, 64)])
    last_name = StringField(
        'Last name', validators=[InputRequired(),
                                 Length(1, 64)])
    email = EmailField(
        'Email', validators=[InputRequired(),
                             Length(1, 64),
                             Email()])
    submit = SubmitField('Invite')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class NewUserForm(InviteUserForm):
    password = PasswordField(
        'Password',
        validators=[
            InputRequired(),
            EqualTo('password2', 'Passwords must match.')
        ])
    password2 = PasswordField('Confirm password', validators=[InputRequired()])

    submit = SubmitField('Create')

class BlogCategoryForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    order = IntegerField('Order', validators=[InputRequired()])
    is_featured = BooleanField("Is Featured ?")
    submit = SubmitField('Submit')


class BlogTagForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    submit = SubmitField('Submit')


class BlogNewsLetterForm(BaseModelForm):
    email = EmailField('Email', validators=[InputRequired(), Length(1, 64), Email(), Unique(BlogNewsLetter.email)])
    submit = SubmitField('Submit')


class BlogPostForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    text = CKEditorField('Body', validators=[InputRequired()])
    image = FileField('Image', validators=[InputRequired(), FileAllowed(images, 'Images only!')])
    categories = QuerySelectMultipleField(
        'Categories',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(BlogCategory).order_by('order'))
    tags = QuerySelectMultipleField(
        'Tags',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(BlogTag).order_by('created_at'))
    newsletter = BooleanField('Send Announcement To Subscribers.')
    all_users = BooleanField('Send Announcement To All Users.')

    submit = SubmitField('Submit')
