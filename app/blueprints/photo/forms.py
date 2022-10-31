from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import ValidationError
from wtforms_alchemy import QuerySelectField, QuerySelectMultipleField
from wtforms.fields import (
    MultipleFileField,
    FileField,
    SubmitField,
    RadioField,
    BooleanField,
    EmailField


)

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


class ImageForm(BaseModelForm):
    image = FileField('Image size (873 × 885 px)', validators=[FileRequired(), FileAllowed(images, 'Images only allowed!')])
    profile_picture = BooleanField('Is Profile picture?', default=False)
    submit = SubmitField('Submit')
