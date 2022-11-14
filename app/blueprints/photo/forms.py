from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms.fields import BooleanField, FileField, SubmitField
from wtforms_alchemy import ModelForm, model_form_factory

from app.common.flask_uploads import IMAGES, UploadSet

BaseModelForm = model_form_factory(FlaskForm)

images = UploadSet('images', IMAGES)


class ImageForm(BaseModelForm):
    image = FileField('Image size (873 × 885 px)',
                      validators=[
                          FileRequired(),
                          FileAllowed(images, 'Images only allowed!')
                      ])
    profile_picture = BooleanField('Is Profile picture?', default=False)
    submit = SubmitField('Submit')
