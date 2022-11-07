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
from wtforms_alchemy import (ModelForm, QuerySelectField,
                             QuerySelectMultipleField, Unique,
                             model_form_factory)

from app.common.flask_uploads import IMAGES, UploadSet

BaseModelForm = model_form_factory(FlaskForm)

images = UploadSet('images', IMAGES)


class PageForm(BaseModelForm):
    name = StringField("Page Name",
                       validators=[DataRequired(),
                                   Length(min=2, max=50)])
    #seo_title = StringField("SEO Title", validators=[DataRequired(), Length(min=2, max=180)])
    #seo_description = StringField("SEO description", validators=[DataRequired(), Length(min=2, max=180)])
    content = CKEditorField("Page content and styling")
    submit = SubmitField('Submit')
