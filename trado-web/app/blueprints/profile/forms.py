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
from flask_uploads import UploadSet, IMAGES

images = UploadSet('images', IMAGES)
docs = UploadSet('docs', ('rtf', 'odf', 'ods', 'gnumeric', 'abw', 'doc', 'docx', 'xls', 'xlsx', 'pdf', 'css'))

BaseModelForm = model_form_factory(FlaskForm)


class PricingForm(FlaskForm):
    title = StringField(" Title e.g 'Free' or 'Premium'")
    is_popular = BooleanField("Is it the popular plan?")
    description = StringField(" Description (Max 250 characters) ")
    button_text = StringField("Button text e.g 'Buy' ")
    button_url = StringField("Call to action url e.g /login ")
    button_type = SelectField(u'Choose button type to display', choices=[('primary','primary'),('secondary','secondary'),('success','success'),
                                                 ('danger','danger'), ('warning','warning'),
                                                 ('info','info'), ('light','light'),
                                                 ('dark','dark'), ('link','link')] ,validators=[DataRequired()])
    submit = SubmitField('Submit')

class PricingAttributeForm(FlaskForm):
    description = StringField(" Description (Max 120 characters) ")
    is_available = BooleanField("Is the feature available under this plan?")
    submit = SubmitField('Submit')

class CostForm(FlaskForm):
    figure = FloatField(" 99.9 ")
    currency = StringField(" GBP or USD etc (Max 120 characters) ")
    currency_icon = StringField(" Currency Icons e.g '£' or '$' or '元' ")
    submit = SubmitField('Submit')


class SlideShowCrudForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=2, max=80)])
    image = FileField('SlideShow Image (928x413)', validators=[FileRequired(), FileAllowed(images, 'Images only allowed!')])
    submit = SubmitField('Submit')

class SeoForm(FlaskForm):
    #meta_tag = SelectField(u'Meta Tag',choices=[('name','name'),('property','property')] ,validators=[DataRequired()])
    title = StringField("Title", validators=[DataRequired(), Length(min=5, max=80)])
    content = StringField("Meta Description, 180 characters maximum", validators=[DataRequired(), Length(min=5, max=181)])
    submit = SubmitField('Submit')

#############################################################
class HomeTextForm(BaseModelForm):
    firstext = StringField("First Title", validators=[DataRequired(), Length(min=5, max=80)])
    secondtext = TextAreaField("Second Title")
    submit = SubmitField('Submit')

class AboutForm(BaseModelForm):
    title = StringField("First Title", validators=[DataRequired(), Length(min=5, max=180)])
    description = CKEditorField("Description")
    submit = SubmitField('Submit')

class CounterForm(BaseModelForm):
    title = StringField("Count Title e.g Projects", validators=[DataRequired(), Length(min=2, max=80)])
    count = StringField("Integers only e.g 1000", validators=[DataRequired(), Length(min=1, max=25)])
    submit = SubmitField('Submit')

class HeadlineForm(BaseModelForm):
    headline = StringField("Headline Title Text")
    description = CKEditorField("Description")
    image = FileField('Images Only')#, FileAllowed(images, 'Images only allowed!'))
    submit = SubmitField('Submit')

class TeamForm(BaseModelForm):
    full_name = StringField("Full Name", validators=[DataRequired(), Length(min=2, max=80)])
    job_title = StringField("Job Title", validators=[DataRequired(), Length(min=2, max=80)])
    image = FileField('Team Member Portrait (255x255)', validators=[FileRequired(), FileAllowed(images, 'Images only allowed!')])
    submit = SubmitField('Submit')

class VideoForm(BaseModelForm):
    title = StringField("Video Title", validators=[DataRequired(), Length(min=2, max=80)])
    url = StringField("url e.g https://www.youtube.com/watch?v=jDDaplaOz7Q", validators=[DataRequired(), Length(min=2, max=80)])
    image = FileField('Video background image (1024 × 760 px)', validators=[FileRequired(), FileAllowed(images, 'Images only allowed!')])
    description = TextAreaField("Description")
    submit = SubmitField('Submit')

class PortfolioForm(BaseModelForm):
    title = StringField("Image Title", validators=[DataRequired(), Length(min=2, max=80)])
    image = FileField('Image size (873 × 885 px)', validators=[FileRequired(), FileAllowed(images, 'Images only allowed!')])
    description = StringField("Description")
    submit = SubmitField('Submit')

class TestimonialForm(BaseModelForm):
    full_name = StringField("Full Name", validators=[DataRequired(), Length(min=2, max=80)])
    job_title = StringField("Job Title ", validators=[DataRequired(), Length(min=2, max=80)])
    comment = StringField("Comment. 250 characters max", validators=[DataRequired(), Length(min=2, max=250)])
    image = FileField('Image size (400 × 400 px) but some templates adjust them automatically.', validators=[FileRequired(), FileAllowed(images, 'Images only allowed!')])
    submit = SubmitField('Submit')

class TemplateSettingForm(BaseModelForm):
    template_name = StringField("Name of template", validators=[DataRequired(), Length(min=2, max=80)])
    category = SelectField(u'Category', choices=[('business','business'),('event','event'),('restaurant','restaurant'),
                                                 ('real estate','real estate'), ('portfolio','portfolio'),
                                                 ('launching soon','launching soon'), ('bare template','bare template')] ,validators=[DataRequired()])
    choice = BooleanField("Is Default Template?")
    image = FileField('Image size (400 × 400 px)', validators=[FileRequired(), FileAllowed(images, 'Images only allowed!')])
    submit = SubmitField('Submit')

class TemplateChoiceForm(BaseModelForm):
    template_name = StringField("Name of template", validators=[DataRequired(), Length(min=2, max=80)])
    choice = BooleanField("Is Default Template?")
    submit = SubmitField('Submit')
    
class NavMenuForm(FlaskForm):
    text = StringField("Text etc Contact", validators=[DataRequired(), Length(min=1, max=80)])
    url = StringField("Url e.g /account/login ", validators=[DataRequired(), Length(min=1, max=80)])
    submit = SubmitField('Submit')
    
class CallToActionForm(FlaskForm):
    text = StringField("Call to action text")
    url = StringField("Call to action url e.g /account/login ")
    show_on_navbar = BooleanField("Should it appear on the navigation bar?")
    is_login = BooleanField("Is this a login button?")
    is_signup = BooleanField("Is this a signup button?")
    button_type = SelectField(u'Choose button type to display', choices=[('primary','primary'),('secondary','secondary'),('success','success'),
                                                 ('danger','danger'), ('warning','warning'),
                                                 ('info','info'), ('light','light'),
                                                 ('dark','dark'), ('link','link')] ,validators=[DataRequired()])
    submit = SubmitField('Submit')

class TechnologiesForm(FlaskForm):
    firstext = StringField("First Title", validators=[DataRequired(), Length(min=5, max=80)])
    secondtext = StringField("Second Title", validators=[DataRequired(), Length(min=10, max=80)])
    submit = SubmitField('Submit')

class ServiceForm(FlaskForm):
    title = StringField("Service Name", validators=[DataRequired(), Length(min=2, max=80)])
    description = StringField("Service Description . Max 250 characters", validators=[DataRequired(), Length(min=10, max=250)])
    action_text = StringField("Service call to action text e.g learn more")
    url = StringField("Call to action url e.g /account/login ")
    icon = StringField("Icon from Flaticons or Font Awesome only e.g shopping-basket", validators=[DataRequired()])
    colour = SelectField(u'Choose colour to display', choices=[('yellow','yellow'),('orange','orange'),('red','red'),
                                                 ('pink','pink'), ('violet','violet'),
                                                 ('purple','purple'), ('blue','blue'),
                                                 ('aqua','aqua'), ('green','green'),('leaf','leaf'),('navy','navy'),
                                                  ('ash','ash'),('white','white')] ,validators=[DataRequired()])
    submit = SubmitField('Submit')

class TrackingScriptForm(FlaskForm):
    name = StringField("Script Name e.g Hotjar or Google Analytics", validators=[DataRequired(), Length(min=2, max=25)])
    script = TextAreaField("Paste the raw script")
    submit = SubmitField('Submit')
    
class ImageTechnologyForm(FlaskForm):
    image = FileField('Technology Image (128x128)', validators=[FileRequired(), FileAllowed(images, 'Images only allowed!')])
    submit = SubmitField('Submit')

class ClientForm(FlaskForm):
    image = FileField('Client Image Max. (400x219)', validators=[FileRequired(), FileAllowed(images, 'Images only allowed!')])
    submit = SubmitField('Submit')
    
class WebsiteLogoForm(BaseModelForm):
    logo_image = FileField('Logo Image (182x33). A transparent logo is better', validators=[FileRequired(), FileAllowed(images, 'Logo Only allowed!')])
    submit = SubmitField('Submit')
    
class BackgroundImageForm(FlaskForm):
    background_image = FileField('Background (1920x1081)', validators=[FileRequired(), FileAllowed(images, 'Images Only allowed!')])
    submit = SubmitField('Submit')

class FaviconImageForm(FlaskForm):
    image = FileField('Favicon (32x32)', validators=[FileRequired(), FileAllowed(images, 'Images Only allowed!')])
    submit = SubmitField('Submit')

class AppleTouchIconForm(FlaskForm):
    favicon_image = FileField('Apple Touch Icon (180x180)', validators=[FileRequired(), FileAllowed(images, 'Images Only allowed!')])
    submit = SubmitField('Submit')
    
# Footer Text Form
class FooterTextForm(BaseModelForm):
    title = CKEditorField("Description and or address", validators=[DataRequired(), Length(min=5)])
    submit = SubmitField('Submit')

# Footer Text Form
class FaqForm(BaseModelForm):
    question = StringField("Question Title", validators=[DataRequired(), Length(min=5)])
    answer = CKEditorField("Answer", validators=[DataRequired(), Length(min=5)])
    submit = SubmitField('Submit')

# Social Media Form 
class SocialMediaIconForm(FlaskForm):
    # image = FileField('Logo Image (128x128)', validators=[FileRequired(), FileAllowed(images, 'Social Iocn Image Only!')])
    icon = StringField("Icon Names only e.g facebook", validators=[DataRequired()])
    url_link = StringField("Icon Link, e.g https://www.facebook.com/Networkedng ", validators=[DataRequired()])
    submit = SubmitField('Submit')
    
# Brand Name Form Model
class BrandNameForm(FlaskForm):
    text = StringField("Brand Name E.g Nokia ", validators=[DataRequired(), Length(min=2, max=15)])
    submit = SubmitField('Submit')

# Copyright Form Model
class CopyRightForm(FlaskForm):
    text = StringField("Copyright Footer Text", validators=[DataRequired(), Length(min=6, max=60)])
    submit = SubmitField('Submit')

# Footer Image Model Form
class FooterImageForm(BaseModelForm):
    image = FileField('Footer Image', validators=[FileRequired(), FileAllowed(images, "Image Allowed Only !")])


# Resource Title Role Model Form
class ResourcesForm(BaseModelForm):
    role_title = StringField("Role Add ...", validators=[DataRequired(), Length(min=3, max=20)])


# Process Form Model
class ProcessForm(FlaskForm):
    steps = StringField("Step to take ", validators=[DataRequired(), Length(min=1, max=120)])
    description = StringField("Description. Max.250 characters" , validators=[DataRequired(), Length(min=1, max=250)])
    #process_icon = StringField("Flaticon or fontawesome icons or leave blank")
    submit = SubmitField('Submit')


# ProcessTitle Area Form Model
class ProcessTitleForm(FlaskForm):
    title = StringField("Process Area Title ", validators=[DataRequired(), Length(min=1, max=250)])
    description = StringField("Description. Max.250 characters" , validators=[DataRequired(), Length(min=1, max=250)])
    image = FileField('Process Area Image 650 by 874px', validators=[FileRequired(), FileAllowed(images, "Image Allowed Only !")])
    submit = SubmitField('Submit')

# ClientTitle Area Form Model
class ClientTitleForm(FlaskForm):
    title = StringField("Client Area Title ", validators=[DataRequired(), Length(min=1, max=250)])
    description = StringField("Description. Max.250 characters" , validators=[DataRequired(), Length(min=1, max=250)])
    submit = SubmitField('Submit')

# PricingTitle Area Form Model
class PricingTitleForm(FlaskForm):
    description = StringField("Description. Max.250 characters" , validators=[DataRequired(), Length(min=1, max=250)])
    submit = SubmitField('Submit')

# TestimonialTitle Area Form Model
class TestimonialTitleForm(FlaskForm):
    title = StringField("Testimonial Area Title ", validators=[DataRequired(), Length(min=1, max=250)])
    description = StringField("Description. Max.250 characters" , validators=[DataRequired(), Length(min=1, max=250)])
    submit = SubmitField('Submit')

#FeatureForm
class FeatureForm(FlaskForm):
    title = StringField("Title or Name", validators=[DataRequired(), Length(min=5, max=80)])
    description = StringField("Description", validators=[DataRequired(), Length(min=10, max=180)])
    icon = StringField("Icon from Semantic UI or Font Awesome only e.g shopping-basket", validators=[DataRequired()])
    submit = SubmitField('Submit')

# FeatureTitle Area Form Model
class FeatureTitleForm(FlaskForm):
    title = StringField("Feature Area Title. Max 250. ", validators=[DataRequired(), Length(min=1, max=250)])
    description = StringField("Description. Max.250 characters" , validators=[DataRequired(), Length(min=1, max=250)])
    submit = SubmitField('Submit')

# ServiceTitle Area Form Model
class ServiceTitleForm(FlaskForm):
    title = StringField("Service Area Title. Max 250. ", validators=[DataRequired(), Length(min=1, max=250)])
    description = StringField("Description. Max.250 characters" , validators=[DataRequired(), Length(min=1, max=250)])
    submit = SubmitField('Submit')
