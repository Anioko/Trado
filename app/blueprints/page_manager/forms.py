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
from wtforms_alchemy import Unique, ModelForm, model_form_factory
from flask_uploads import UploadSet, IMAGES

BaseModelForm = model_form_factory(FlaskForm)

images = UploadSet('images', IMAGES)


class PageForm(BaseModelForm):
    name = StringField("Page Name", validators=[DataRequired(), Length(min=2, max=50)])
    #seo_title = StringField("SEO Title", validators=[DataRequired(), Length(min=2, max=180)])
    #seo_description = StringField("SEO description", validators=[DataRequired(), Length(min=2, max=180)])
    content = CKEditorField("Page content and styling")
    submit = SubmitField('Submit')
