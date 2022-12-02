from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms_alchemy import model_form_factory

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
