from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required
from flask_rq import get_queue
from flask_ckeditor import upload_success
from flask_sqlalchemy import Pagination

from app import db
#from app.admin.forms import (
    #ChangeAccountTypeForm,
    #ChangeUserEmailForm,
    #InviteUserForm,
    #NewUserForm,
#)
from app.decorators import admin_required
from app.email import send_email
from app.models import *
from app.models.content_manager import Headline
from app.blueprints.content_manager.forms import *

content_manager = Blueprint('content_manager', __name__)


@content_manager.route('/content/setting')
@login_required
def index():
    return render_template('content_manager/index.html')

####################Content Management System Start #################




@content_manager.route('/slideshows-list')
@login_required
def added_slideshows():
    """View all registered users."""
    slideshow = SlideShowImage.query.all()
    if slideshow is None:
        return redirect(url_for('content_manager.add_slideshows'))
    return render_template(
        'content_manager/slideshows/added_slideshows.html', slideshow=slideshow)

@content_manager.route('/slideshows/add_slideshow', methods=['GET', 'POST'])
@login_required
def add_slideshow():
    form = SlideShowCrudForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            title = form.title.data
            image = images.save(request.files['image'])
            slideshow = SlideShowImage(title=title,image_filename=image)
            db.session.add(slideshow)
            db.session.commit()
            flash("SlideShow added successfully .", "success")
            return redirect(url_for("content_manager.added_slideshows"))
    
    return render_template("content_manager/slideshows/add_slideshow.html", form=form)

@content_manager.route('/slideshows/<int:slideshow_id>/_delete', methods=['GET', 'POST'])
@login_required
def delete_slideshow(slideshow_id):
    """Delete the item """
    slideshows = SlideShowImage.query.filter_by(id=slideshow_id).first()
    db.session.commit()
    db.session.delete(slideshows)
    flash('Successfully deleted ' , 'success')
    return redirect(url_for('content_manager.added_slideshows'))


# Added Headline
@content_manager.route('/headline-list')
@login_required
def added_headline():
    """View all added headline content."""
    data = Headline.query.all()
    if data is None:
        return redirect(url_for('content_manager.add_headline'))
    return render_template(
        'content_manager/headline/added_headline.html', data=data)

# Add Headline 
@content_manager.route('/headline/headline', methods=['POST', 'GET'])
@login_required
def add_headline():
    form = HeadlineForm()
    if form.validate_on_submit():
        data = Headline(
            headline = form.headline.data,
            description = form.description.data,
            image = images.save(request.files['image'])
            )
        db.session.add(data)
        db.session.commit()
        flash("Headline Text Added Successfully.", "success")
        return redirect(url_for('content_manager.added_headline'))
    return render_template('content_manager/headline/add_headline.html', form=form)

# Edit Headline
@content_manager.route('/headline/<int:id>/edit', methods=['POST', 'GET'])
@login_required
def edit_headline(id):
    data = Headline.query.filter_by(id=id).first()
    form = HeadlineForm(obj=data)
    if form.validate_on_submit():
        data.headline = form.headline.data,
        data.description = form.description.data,
        data.image = images.save(request.files['image']),
        db.session.add(data)
        db.session.commit()
        flash("Headline Text Added Successfully.", "success")
        return redirect(url_for('content_manager.added_headline'))
    else:
        flash('ERROR! Content was not edited.', 'error')
    return render_template('content_manager/headline/add_headline.html', form=form)

@content_manager.route('/headline/<int:id>/_delete', methods=['GET', 'POST'])
@login_required
def delete_headline(id):
    """Delete the item """
    data = Headline.query.filter_by(id=id).first()
    db.session.commit()
    db.session.delete(data)
    flash('Successfully deleted ' , 'success')
    return redirect(url_for('content_manager.added_headline'))

@content_manager.route('/images-list')
@login_required
def added_images():
    """View all added images to the public area under the Information/Tech area."""
    images = TechnologiesImage.query.all()
    if images is None:
        return redirect(url_for('content_manager.add_image'))
    return render_template(
        'content_manager/images/added_images.html', slideshow=images)

@content_manager.route('/images/add_image', methods=['GET', 'POST'])
@login_required
def add_image():
    form = ImageTechnologyForm()
    if request.method == 'POST':
        image = images.save(request.files['image'])
        technology_img = TechnologiesImage(image=image)
        db.session.add(technology_img)
        db.session.commit()
        flash("Technology Added Successfully .", "success")
        return redirect(url_for('content_manager.added_images'))
    return render_template("content_manager/images/add_image.html", form=form)

'''
##needless to edit, just delete is enough
@content_manager.route('/images/<int:image_id>/edit', methods=['POST', 'GET'])

def edit_image(image_id):
    image_data = TechnologiesImage.query.get(image_id)
    form = ImageTechnologyForm(obj=image_data)
    form.image.validators = form.image.validators[1:]
    form.image.validators.insert(0, Optional())
    form.image.flags.required = False
    if request.method == 'POST':
        if request.files['image']:
            image = images.save(request.files['image'])
            if os.path.exists(image_data.image_path):
                os.remove(image_data.image_path)
            image_data.image_filename = image
        db.session.add(image_data)
        db.session.commit()
        flash("Technology Image Updated Successfully.", "success")
        return redirect(url_for("content_manager.technology_image"))
    return render_template("content_manager/images/edit_image.html", form=form, image_data=image_data)
'''
# delete image 
@content_manager.route('/images/delete/<int:image_id>', methods=['GET', 'POST'])
@login_required
def delete_image(image_id):
    data = TechnologiesImage.query.get(image_id)
    db.session.delete(data)
    db.session.commit()
    flash("Technology Image deleted Successfully.", "success")
    return redirect(url_for('content_manager.added_images'))

# Add Client
@content_manager.route('/clients')
@login_required
def added_client():
    """View all added client logos to the landing page"""
    data = Client.query.all()
    if data is None:
        return redirect(url_for('content_manager.add_client'))
    return render_template(
        'content_manager/client/added_client.html', data=data)

@content_manager.route('/clients/add_client', methods=['GET', 'POST'])
@login_required
def add_client():
    form = ClientForm()
    if request.method == 'POST':
        image = images.save(request.files['image'])
        data = Client(image=image)
        db.session.add(data)
        db.session.commit()
        flash("Client logo Added Successfully .", "success")
        return redirect(url_for('content_manager.added_client'))
    return render_template("content_manager/client/add_client.html", form=form)


# delete client 
@content_manager.route('/clients/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_client(id):
    data = Client.query.get(id)
    db.session.delete(data)
    db.session.commit()
    flash("Client logo deleted Successfully.", "success")
    return redirect(url_for('content_manager.added_client'))


# Added Features
@content_manager.route('/feature')
@login_required
def added_feature():
    """View added feature and description."""
    data = Feature.query.all()
    if data is None:
        return redirect(url_for('content_manager.add_feature'))
    return render_template(
        'content_manager/feature/added_feature.html', data=data)

# Add Feature Area
@content_manager.route('/feature/add', methods=['POST', 'GET'])
@login_required
def add_feature():
    form = FeatureForm()
    if form.validate_on_submit():
        data = Feature(
            title=form.title.data,
            description=form.description.data,
            icon=form.icon.data
            )
        db.session.add(data)
        db.session.commit()
        flash("Added Successfully.", "success")
        return redirect(url_for('content_manager.added_feature'))
    return render_template('content_manager/feature/add_feature.html', form=form)

# Edit Feature Area
@content_manager.route('/feature/<int:id>/edit', methods=['POST', 'GET'])
@login_required
def edit_feature(id):
    data = Feature.query.filter_by(id=id).first()
    form = FeatureForm(obj=data)
    if form.validate_on_submit():
        data.title=form.title.data
        data.description=form.description.data
        data.icon=form.icon.data
        db.session.add(data)
        db.session.commit()
        flash("Edited Successfully.", "success")
        return redirect(url_for('content_manager.added_feature'))
    else:
        flash('ERROR! Data was not edited.', 'error')
    return render_template('content_manager/feature/add_feature.html', form=form)

@content_manager.route('/feature/<int:id>/_delete', methods=['GET', 'POST'])
@login_required
def delete_feature(id):
    """Delete the item """
    data = Feature.query.filter_by(id=id).first()
    db.session.commit()
    db.session.delete(data)
    flash('Successfully deleted ' , 'success')
    return redirect(url_for('content_manager.added_feature'))


@content_manager.route('/calltoaction-list')
@login_required
def added_calltoaction():
    """View all added call to actin text."""
    data = CallToAction.query.all()
    if data is None:
        return redirect(url_for('content_manager.add_call_to_action'))
    return render_template(
        'content_manager/calltoaction/added_calltoaction.html', data=data)

# Add CallToAction 
@content_manager.route('/calltoaction/call_to_action', methods=['POST', 'GET'])
@login_required
def add_call_to_action():
    form = CallToActionForm()
    if form.validate_on_submit():
        data = CallToAction(
            text=form.text.data,
            url=form.url.data,
            button_type = form.button_type.data,
            show_on_navbar=form.show_on_navbar.data,
            is_login=form.is_login.data,
            is_signup=form.is_signup.data,
            )
        db.session.add(data)
        db.session.commit()
        flash("Call To Action Text Added Successfully.", "success")
        return redirect(url_for('content_manager.added_calltoaction'))
    return render_template('content_manager/calltoaction/add_call_to_action.html', form=form)

# Edit CallToAction
@content_manager.route('/calltaction/<int:id>/edit', methods=['POST', 'GET'])
@login_required
def edit_calltoaction(id):
    data = CallToAction.query.filter_by(id=id).first()
    form = CallToActionForm(obj=data)
    if form.validate_on_submit():
        data.text=form.text.data
        data.url=form.url.data
        data.button_type = form.button_type.data
        data.show_on_navbar=form.show_on_navbar.data
        data.is_login=form.is_login.data
        data.is_signup=form.is_signup.data
        db.session.add(data)
        db.session.commit()
        flash("Call To Action Text Added Successfully.", "success")
        return redirect(url_for('content_manager.added_calltoaction'))
    else:
        flash('ERROR! Content was not edited.', 'error')
    return render_template('content_manager/calltoaction/add_call_to_action.html', form=form)

@content_manager.route('/calltoaction/<int:id>/_delete', methods=['GET', 'POST'])
@login_required
def delete_calltoaction(id):
    """Delete the item """
    data = CallToAction.query.filter_by(id=id).first()
    db.session.commit()
    db.session.delete(data)
    flash('Successfully deleted ' , 'success')
    return redirect(url_for('content_manager.added_calltoaction'))



# Add Navbar items 
@content_manager.route('/navigation/menu', methods=['POST', 'GET'])
@login_required
def add_navmenu():
    form = NavMenuForm()
    if form.validate_on_submit():
        data = NavMenu(
            text=form.text.data,
            url=form.url.data
            )
        db.session.add(data)
        db.session.commit()
        flash("Navigation menu item added successfully.", "success")
        return redirect(url_for('content_manager.added_navmenu'))
    return render_template('content_manager/nav_menu.html', form=form)



@content_manager.route('/navmenu-list')
@login_required
def added_navmenu():
    """View all added navigations."""
    data = NavMenu.query.all()
    return render_template(
        'content_manager/added_navmenu.html', data=data)

@content_manager.route('/navmenu/<int:id>/_delete', methods=['GET', 'POST'])
@login_required
def delete_navmenu(id):
    """Delete the item """
    data = NavMenu.query.filter_by(id=id).first()
    db.session.commit()
    db.session.delete(data)
    flash('Successfully deleted ' , 'success')
    return redirect(url_for('content_manager.added_navmenu'))




@content_manager.route('/hometext', methods=['GET', 'POST'])
@login_required
def home_text():
    """Create a new text for the home page."""
    item = HomeText.query.first()
    if item is not None:
        return redirect(url_for('content_manager.added_hometext'))
        
    form = HomeTextForm()
    if form.validate_on_submit():
        data = HomeText(
            firstext=form.firstext.data,
            secondtext=form.secondtext.data)
        db.session.add(data)
        db.session.commit()
        flash('HomeText {} successfully created'.format(data.firstext),
              'form-success')
        return redirect(url_for('content_manager.added_hometext'))
    return render_template('content_manager/hometext/add_hometext.html', form=form)

@content_manager.route('/hometext-list')
@login_required
def added_hometext():
    """View all added texts."""
    data = HomeText.query.first()
    return render_template(
        'content_manager/hometext/added_hometext.html', data=data)

@content_manager.route('/hometext/<int:id>/_delete', methods=['GET', 'POST'])

def delete_hometext(id):
    """Delete the home text """
    data = HomeText.query.filter_by(id=id).first()
    db.session.commit()
    db.session.delete(data)
    flash('Successfully deleted ' , 'success')
    return redirect(url_for('content_manager.home_text'))


@content_manager.route('/information-list')
@login_required
def added_information():
    """View all added call to actin text."""
    data = TechnologiesText.query.all()
    if data is None:
        return redirect(url_for('content_manager.add_information'))
    return render_template(
        'content_manager/information/added_information.html', data=data)

# Add Information to Public Page
@content_manager.route('/information/add', methods=['POST', 'GET'])
@login_required
def add_information():
    form = TechnologiesForm()
    if form.validate_on_submit():
        data = TechnologiesText(
            firstext = form.firstext.data,
            secondtext = form.secondtext.data
            )
        db.session.add(data)
        db.session.commit()
        flash("Text Added Successfully.", "success")
        return redirect(url_for('content_manager.added_information'))
    return render_template('content_manager/information/add_information.html', form=form)

@content_manager.route('/information/<int:id>/_delete', methods=['GET', 'POST'])
@login_required
def delete_information(id):
    """Delete the information added """
    data = TechnologiesText.query.filter_by(id=id).first()
    db.session.commit()
    db.session.delete(data)
    flash('Successfully deleted ' , 'success')
    if data is None:
        return redirect(url_for('content_manager.add_information'))
    return redirect(url_for('content_manager.added_information'))



#Add Count

@content_manager.route('/counter')
@login_required
def added_count():
    """View all added counts."""
    data = Counter.query.all()
    if data is None:
        return redirect(url_for('content_manager.add_counter'))
    return render_template(
        'content_manager/counter/added_counters.html', data=data)

@content_manager.route('/count/add', methods=['POST', 'GET'])

def add_count():
    form = CounterForm()
    if form.validate_on_submit():
        data = Counter(
            title = form.title.data,
            count = form.count.data
            )
        db.session.add(data)
        db.session.commit()
        flash("Count Added Successfully.", "success")
        return redirect(url_for('content_manager.added_count'))
    return render_template('content_manager/counter/add_count.html', form=form)

@content_manager.route('/count/<int:id>/_delete', methods=['GET', 'POST'])
@login_required
def delete_count(id):
    """Delete the count added """
    data = Counter.query.filter_by(id=id).first()
    db.session.commit()
    db.session.delete(data)
    flash('Successfully deleted ' , 'success')
    if data is None:
        return redirect(url_for('content_manager.add_count'))
    return redirect(url_for('content_manager.added_count'))

# Add Service
@content_manager.route('/services')
@login_required
def added_services():
    """View all added services."""
    data = Service.query.all()
    if data is None:
        return redirect(url_for('content_manager.add_service'))
    return render_template(
        'content_manager/service/added_services.html', data=data)


@content_manager.route('/service/add', methods=['POST', 'GET'])
@login_required
def add_service():
    form = ServiceForm()
    if form.validate_on_submit():
        data = Service(
            title = form.title.data,
            description = form.description.data,
             action_text = form.action_text.data,
             url = form.url.data,
             icon = form.icon.data,
             color = form.colour.data
            )
        db.session.add(data)
        db.session.commit()
        flash("Text Added Successfully.", "success")
        return redirect(url_for('content_manager.added_services'))
    return render_template('content_manager/service/add_service.html', form=form)

# Edit Service Area
@content_manager.route('/service/<int:id>/edit', methods=['POST', 'GET'])
@login_required
def edit_service(id):
    data = Service.query.filter_by(id=id).first()
    form = ServiceForm(obj=data)
    if form.validate_on_submit():
        data.title=form.title.data
        data.description=form.description.data
        data.action_text = form.action_text.data,
        data.url = form.url.data
        data.icon = form.icon.data
        data.colour = form.colour.data
        db.session.add(data)
        db.session.commit()
        flash("Edited Successfully.", "success")
        return redirect(url_for('content_manager.added_services'))
    else:
        flash('ERROR! Data was not edited.', 'error')
    return render_template('content_manager/service/add_service.html', form=form)

@content_manager.route('/service/<int:id>/_delete', methods=['GET', 'POST'])
@login_required
def delete_service(id):
    """Delete the information added """
    data = Service.query.filter_by(id=id).first()
    db.session.commit()
    db.session.delete(data)
    flash('Successfully deleted ' , 'success')
    if data is None:
        return redirect(url_for('content_manager.add_service'))
    return redirect(url_for('content_manager.added_services'))

# Add Faq
@content_manager.route('/faq')
@login_required
def added_faq():
    """View all added faq."""
    data = Faq.query.all()
    if data is None:
        return redirect(url_for('content_manager.add_faq'))
    return render_template(
        'content_manager/faq/added_faq.html', data=data)


@content_manager.route('/faq/add', methods=['POST', 'GET'])
@login_required
def add_faq():
    form = FaqForm()
    if form.validate_on_submit():
        data = Faq(
            question = form.question.data,
            answer = form.answer.data
            )
        db.session.add(data)
        db.session.commit()
        flash("Text Added Successfully.", "success")
        return redirect(url_for('content_manager.added_faq'))
    return render_template('content_manager/faq/add_faq.html', form=form)


@content_manager.route('/faq/<int:id>/_delete', methods=['GET', 'POST'])
@login_required
def delete_faq(id):
    """Delete the information added """
    data = Faq.query.filter_by(id=id).first()
    db.session.commit()
    db.session.delete(data)
    flash('Successfully deleted ' , 'success')
    if data is None:
        return redirect(url_for('content_manager.add_faq'))
    return redirect(url_for('content_manager.added_faq'))


# Add Team Members
@content_manager.route('/members')
@login_required
def added_members():
    """View all added team members."""
    data = Team.query.all()
    if data is None:
        return redirect(url_for('content_manager.add_member'))
    return render_template(
        'content_manager/team/added_members.html', data=data)


@content_manager.route('/member/add', methods=['POST', 'GET'])
@login_required
def add_member():
    form = TeamForm()
    if form.validate_on_submit():
        data = Team(
            full_name = form.full_name.data,
            job_title = form.job_title.data,
            image = images.save(request.files['image'])
            )
        db.session.add(data)
        db.session.commit()
        flash("Text Added Successfully.", "success")
        return redirect(url_for('content_manager.added_members'))
    return render_template('content_manager/team/add_member.html', form=form)

@content_manager.route('/member/<int:id>/_delete', methods=['GET', 'POST'])
@login_required
def delete_member(id):
    """Delete the information added """
    data = Team.query.filter_by(id=id).first()
    db.session.commit()
    db.session.delete(data)
    flash('Successfully deleted ' , 'success')
    if data is None:
        return redirect(url_for('content_manager.add_member'))
    return redirect(url_for('content_manager.added_members'))


# Add Video
@content_manager.route('/video')
@login_required
def added_video():
    """View added video."""
    data = Video.query.first()
    if data is None:
        return redirect(url_for('content_manager.add_video'))
    return render_template(
        'content_manager/video/added_video.html', data=data)


@content_manager.route('/video/add', methods=['POST', 'GET'])
@login_required
def add_video():
    form = VideoForm()
    if form.validate_on_submit():
        data = Video(
            title = form.title.data,
            url = form.url.data,
            description = form.description.data,
            image = images.save(request.files['image'])
            )
        db.session.add(data)
        db.session.commit()
        flash("Video Added Successfully.", "success")
        return redirect(url_for('content_manager.added_video'))
    return render_template('content_manager/video/add_video.html', form=form)

@content_manager.route('/video/<int:id>/_delete', methods=['GET', 'POST'])
@login_required
def delete_video(id):
    """Delete the video added """
    data = Video.query.filter_by(id=id).first()
    db.session.commit()
    db.session.delete(data)
    flash('Successfully deleted ' , 'success')
    if data is None:
        return redirect(url_for('content_manager.add_video'))
    return redirect(url_for('content_manager.added_video'))


# Add Portfolio
@content_manager.route('/portfolio')
@login_required
def added_portfolio():
    """View added portfolio."""
    data = Portfolio.query.all()
    if data is None:
        return redirect(url_for('content_manager.add_portfolio'))
    return render_template(
        'content_manager/portfolio/added_portfolio.html', data=data)


@content_manager.route('/portfolio/add', methods=['POST', 'GET'])
@login_required
def add_portfolio():
    form = PortfolioForm()
    if form.validate_on_submit():
        data = Portfolio(
            title = form.title.data,
            description = form.description.data,
            image = images.save(request.files['image'])
            )
        db.session.add(data)
        db.session.commit()
        flash("Portfolio Added Successfully.", "success")
        return redirect(url_for('content_manager.added_portfolio'))
    return render_template('content_manager/portfolio/add_portfolio.html', form=form)

@content_manager.route('/portfolio/<int:id>/_delete', methods=['GET', 'POST'])
@login_required
def delete_portfolio(id):
    """Delete the portfolio added """
    data = Portfolio.query.filter_by(id=id).first()
    db.session.commit()
    db.session.delete(data)
    flash('Successfully deleted ' , 'success')
    if data is None:
        return redirect(url_for('content_manager.add_portfolio'))
    return redirect(url_for('content_manager.added_portfolio'))

# Add Testimonial
@content_manager.route('/testimonial')
@login_required
def added_testimonial():
    """View added testimonial."""
    data = Testimonial.query.all()
    if data is None:
        return redirect(url_for('content_manager.add_testimonial'))
    return render_template(
        'content_manager/testimonial/added_testimonial.html', data=data)


@content_manager.route('/testimonial/add', methods=['POST', 'GET'])
@login_required
def add_testimonial():
    form = TestimonialForm()
    if form.validate_on_submit():
        data = Testimonial(
            full_name = form.full_name.data,
            job_title = form.job_title.data,
            comment = form.comment.data,
            image = images.save(request.files['image'])
            )
        db.session.add(data)
        db.session.commit()
        flash("Testimonial Added Successfully.", "success")
        return redirect(url_for('content_manager.added_testimonial'))
    return render_template('content_manager/testimonial/add_testimonial.html', form=form)

@content_manager.route('/testimonial/<int:id>/_delete', methods=['GET', 'POST'])
@login_required
def delete_testimonial(id):
    """Delete the testimonial added """
    data = Testimonial.query.filter_by(id=id).first()
    db.session.commit()
    db.session.delete(data)
    flash('Successfully deleted ' , 'success')
    if data is None:
        return redirect(url_for('content_manager.add_testimonial'))
    return redirect(url_for('content_manager.added_testimonial'))

# Add Background-Image

@content_manager.route('/background-image')
@login_required
def added_background_image():
    """View available background image"""
    data = BackgroundImage.query.first()
    if data is None:
        return redirect(url_for('content_manager.add_background_image'))
    return render_template(
        'content_manager/background/added_images.html', data=data)

# Background Image add method
@content_manager.route('/background_image/add', methods=['POST', 'GET'])

def add_background_image():
    form = BackgroundImageForm(request.form)
    if request.method == 'POST':
        image = images.save(request.files['background_image'])
        background_image = BackgroundImage(background_image=image)
        db.session.add(background_image)
        db.session.commit()
        flash("Background Added Successfully .", "success")
        return redirect(url_for('content_manager.added_background_image'))
    return render_template('content_manager/background/add_image.html', form=form)

# Background Image Delete Method 
@content_manager.route('/background_image/delete/<int:background_image_id>', methods=['POST', 'GET'])

def delete_background_image(background_image_id):
    background_image_data = BackgroundImage.query.get(background_image_id)
    db.session.delete(background_image_data)
    db.session.commit()
    flash("Image Deleted Successfully.", "success")
    return redirect(url_for('content_manager.added_background_image'))

@content_manager.route('/logo')
@login_required
def added_logo():
    """View available logo image"""
    data = Logo.query.first()
    if data is None:
        return redirect(url_for('content_manager.add_logo'))
    return render_template(
        'content_manager/logo/added_logo.html', data=data)

# Logo add method
@content_manager.route('/logo/add', methods=['POST', 'GET'])
@login_required
def add_logo():
    form = WebsiteLogoForm(request.form)
    if request.method == 'POST':
        image = images.save(request.files['logo_image'])
        logo = Logo(logo_image=image)
        db.session.add(logo)
        db.session.commit()
        flash("Logo Added Successfully .", "success")
        return redirect(url_for('content_manager.added_logo'))
    return render_template('content_manager/logo/add_logo.html', form=form)

# Logo Delete Method 
@content_manager.route('/logo/delete/<int:logo_id>', methods=['POST', 'GET'])
@login_required
def delete_logo(logo_id):
    logo_data = Logo.query.get(logo_id)
    db.session.delete(logo_data)
    db.session.commit()
    flash("Logo Deleted Successfully.", "success")
    return redirect(url_for('content_manager.add_logo'))

@content_manager.route('/brandname', methods=['GET', 'POST'])
@login_required
def add_brand_name():
    """Add a new brand name."""
    item = BrandName.query.first()
    if item is not None:
        return redirect(url_for('content_manager.added_brandname'))
        
    form = BrandNameForm()
    if form.validate_on_submit():
        data = BrandName(
            text=form.text.data
            )
        db.session.add(data)
        db.session.commit()
        flash('BrandName {} successfully created'.format(data.text),
              'form-success')
        return redirect(url_for('content_manager.added_brandname'))
    return render_template('content_manager/brandname/add_brandname.html', form=form)

@content_manager.route('/brandname-list')
@login_required
def added_brandname():
    """View added brand name."""
    data = BrandName.query.first()
    return render_template(
        'content_manager/brandname/added_brandname.html', data=data)

@content_manager.route('/brandname/<int:id>/_delete', methods=['GET', 'POST'])
@login_required
def delete_brandname(id):
    """Delete the brand name """
    data = BrandName.query.filter_by(id=id).first()
    db.session.commit()
    db.session.delete(data)
    flash('Successfully deleted ' , 'success')
    return redirect(url_for('content_manager.add_brand_name'))

@content_manager.route('/seo-list')
@login_required

def added_seo():
    """View all added SEO texts."""
    data = Seo.query.first()
    if data is None:
        return redirect(url_for('content_manager.add_seo'))
    return render_template(
        'content_manager/seo/added_seo.html', data=data)

# Add SEO 
@content_manager.route('/seo/add', methods=['POST', 'GET'])
def add_seo():
    form = SeoForm()
    if form.validate_on_submit():
        data = Seo(
            title=form.title.data,
            content=form.content.data
            )
        db.session.add(data)
        db.session.commit()
        flash("SEO Added Successfully.", "success")
        return redirect(url_for('content_manager.added_seo'))
    return render_template('content_manager/seo/add_seo.html', form=form)

# Edit SEO 
@content_manager.route('/seo/<int:id>/edit', methods=['POST', 'GET'])
@login_required
def edit_seo(id):
    data = Seo.query.filter_by(id=id).first()
    form = SeoForm(obj=data)
    if form.validate_on_submit():
        data.title=form.title.data
        data.content=form.content.data
        db.session.add(data)
        db.session.commit()
        flash("SEO Added Successfully.", "success")
        return redirect(url_for('content_manager.added_seo'))
    else:
        flash('ERROR! SEO was not edited.', 'error')
    return render_template('content_manager/seo/add_seo.html', form=form)

@content_manager.route('/seo/<int:id>/_delete', methods=['GET', 'POST'])
def delete_seo(id):
    """Delete the seo texts """
    data = Seo.query.filter_by(id=id).first()
    db.session.commit()
    db.session.delete(data)
    flash('Successfully deleted ' , 'success')
    if data is None:
        return redirect(url_for('content_manager.add_seo'))
    return redirect(url_for('content_manager.added_seo'))


@content_manager.route('/footertext-list')
@login_required
def added_footertext():
    """View added footer text."""
    data = FooterText.query.first()
    if data is None:
        return redirect(url_for('content_manager.add_footertext'))
    return render_template(
        'content_manager/footertext/added_footertext.html', data=data)

# Add FooterText 
@content_manager.route('/footer/add', methods=['POST', 'GET'])

def add_footertext():
    form = FooterTextForm()
    if form.validate_on_submit():
        data = FooterText(
            title=form.title.data
            )
        db.session.add(data)
        db.session.commit()
        flash("Footer Text Added Successfully.", "success")
        return redirect(url_for('content_manager.added_footertext'))
    return render_template('content_manager/footertext/add_footertext.html', form=form)


# Edit Footer 
@content_manager.route('/footertext/<int:id>/edit', methods=['POST', 'GET'])
@login_required
def edit_footertext(id):
    data = FooterText.query.filter_by(id=id).first()
    form = FooterTextForm(obj=data)
    if form.validate_on_submit():
        data.title=form.title.data
        db.session.add(data)
        db.session.commit()
        flash("Edit successfully.", "success")
        return redirect(url_for('content_manager.added_footertext'))
    else:
        flash('ERROR! Text was not edited.', 'error')
    return render_template('content_manager/footertext/add_footertext.html', form=form)

@content_manager.route('/footer/<int:id>/_delete', methods=['GET', 'POST'])
@login_required
def delete_footertext(id):
    """Delete the item """
    data = FooterText.query.filter_by(id=id).first()
    db.session.commit()
    db.session.delete(data)
    flash('Successfully deleted ' , 'success')
    return redirect(url_for('content_manager.added_footertext'))

@content_manager.route('/icon-list')
@login_required
def added_icons():
    """View all added icons."""
    data = SocialMediaIcon.query.all()
    if data is None:
        return redirect(url_for('content_manager.add_icon'))
    return render_template(
        'content_manager/icon/added_icon.html', data=data)

# Add Icon 
@content_manager.route('/icon/add', methods=['POST', 'GET'])

def add_icon():
    form = SocialMediaIconForm()
    if form.validate_on_submit():
        data = SocialMediaIcon(
            icon=form.icon.data,
            url_link=form.url_link.data
            )
        db.session.add(data)
        db.session.commit()
        flash("Icon Added Successfully.", "success")
        return redirect(url_for('content_manager.added_icons'))
    return render_template('content_manager/icon/add_icon.html', form=form)

# Edit Icon 
@content_manager.route('/icon/<int:id>/edit', methods=['POST', 'GET'])
@login_required
def edit_icon(id):
    data = SocialMediaIcon.query.filter_by(id=id).first()
    form = SocialMediaIconForm(obj=data)
    if form.validate_on_submit():
        data.icon=form.icon.data
        data.url_link=form.url_link.data
        db.session.add(data)
        db.session.commit()
        flash("Icon Added Successfully.", "success")
        return redirect(url_for('content_manager.added_icons'))
    else:
        flash('ERROR! icon was not edited.', 'error')
    return render_template('content_manager/icon/add_icon.html', form=form)

@content_manager.route('/icon/<int:id>/_delete', methods=['GET', 'POST'])

def delete_icon(id):
    """Delete the item """
    data = SocialMediaIcon.query.filter_by(id=id).first()
    db.session.commit()
    db.session.delete(data)
    flash('Successfully deleted ' , 'success')
    return redirect(url_for('content_manager.added_icons'))

# Add About us
@content_manager.route('/about')
@login_required
def added_about():
    """View added about us text."""
    data = About.query.first()
    if data is None:
        return redirect(url_for('content_manager.add_about'))
    return render_template(
        'content_manager/about/added_about.html', data=data)

 
@content_manager.route('/about/add', methods=['POST', 'GET'])
@login_required
def add_about():
    form = AboutForm()
    if form.validate_on_submit():
        data = About(
            title=form.title.data,
            description=form.description.data
            )
        db.session.add(data)
        db.session.commit()
        flash("Added Successfully.", "success")
        return redirect(url_for('content_manager.added_about'))
    return render_template('content_manager/about/add_about.html', form=form)


# Edit About
@content_manager.route('/about/<int:id>/edit', methods=['POST', 'GET'])
@login_required
def edit_about(id):
    data = About.query.filter_by(id=id).first()
    form = AboutForm(obj=data)
    if form.validate_on_submit():
        data.title=form.title.data,
        data.description=form.description.data
        db.session.add(data)
        db.session.commit()
        flash("Edit successfully.", "success")
        return redirect(url_for('content_manager.added_about'))
    else:
        flash('ERROR! Text was not edited.', 'error')
    return render_template('content_manager/about/add_about.html', form=form)

@content_manager.route('/about/<int:id>/_delete', methods=['GET', 'POST'])

def delete_about(id):
    """Delete the item """
    data = About.query.filter_by(id=id).first()
    db.session.commit()
    db.session.delete(data)
    flash('Successfully deleted ' , 'success')
    return redirect(url_for('content_manager.added_about'))


# Add CopyRight 
@content_manager.route('/copyright-list')
@login_required
def added_copyright():
    """View added copyright text."""
    data = CopyRight.query.first()
    if data is None:
        return redirect(url_for('content_manager.add_copyright'))
    return render_template(
        'content_manager/copyright/added_copyright.html', data=data)


@content_manager.route('/copyright/add', methods=['POST', 'GET'])
@login_required
def add_copyright():
    form = CopyRightForm()
    if form.validate_on_submit():
        data = CopyRight(
            text=form.text.data
            )
        db.session.add(data)
        db.session.commit()
        flash("CopyRight Text Added Successfully.", "success")
        return redirect(url_for('content_manager.added_copyright'))
    return render_template('content_manager/copyright/add_copyright.html', form=form)


# Edit Copyright
@content_manager.route('/copyright/<int:id>/edit', methods=['POST', 'GET'])
@login_required
def edit_copyright(id):
    data = CopyRight.query.filter_by(id=id).first()
    form = CopyRightForm(obj=data)
    if form.validate_on_submit():
        data.text=form.text.data
        db.session.add(data)
        db.session.commit()
        flash("Edit successfully.", "success")
        return redirect(url_for('content_manager.added_copyright'))
    else:
        flash('ERROR! Text was not edited.', 'error')
    return render_template('content_manager/copyright/add_copyright.html', form=form)

@content_manager.route('/copyright/<int:id>/_delete', methods=['GET', 'POST'])
@login_required
def delete_copyright(id):
    """Delete the item """
    data = CopyRight.query.filter_by(id=id).first()
    db.session.commit()
    db.session.delete(data)
    flash('Successfully deleted ' , 'success')
    return redirect(url_for('content_manager.added_copyright'))

#Favicon

@content_manager.route('/favicon-image')
@login_required
def added_favicon_image():
    """View available favicon image"""
    data = FaviconImage.query.first()
    if data is None:
        return redirect(url_for('content_manager.add_favicon_image'))
    return render_template(
        'content_manager/favicon/added_images.html', data=data)

# Favicon Image add method
@content_manager.route('/favicon_image/add', methods=['POST', 'GET'])
@login_required
def add_favicon_image():
    form = FaviconImageForm(request.form)
    if request.method == 'POST':
        image = images.save(request.files['image'])
        image = FaviconImage(image=image)
        db.session.add(image)
        db.session.commit()
        flash("Favicon Added Successfully .", "success")
        return redirect(url_for('content_manager.added_favicon_image'))
    return render_template('content_manager/favicon/add_image.html', form=form)

# Favicon Image Delete Method 
@content_manager.route('/favicon_image/delete/<int:favicon_image_id>', methods=['POST', 'GET'])
@login_required
def delete_favicon_image(favicon_image_id):
    favicon_image_data = FaviconImage.query.get(favicon_image_id)
    db.session.delete(favicon_image_data)
    db.session.commit()
    flash("Image Deleted Successfully.", "success")
    return redirect(url_for('content_manager.added_favicon_image'))

#Apple Touch Icon

@content_manager.route('/apple_touch_icon')
@login_required
def added_apple_touch_icon():
    """View available favicon image"""
    data = AppleTouchIcon.query.first()
    if data is None:
        return redirect(url_for('content_manager.add_apple_touch_icon'))
    return render_template(
        'content_manager/apple_touch_icon/added_apple_touch_icon.html', data=data)

# Favicon Image add method
@content_manager.route('/apple_touch_icon/add', methods=['POST', 'GET'])
@login_required
def add_apple_touch_icon():
    form = AppleTouchIconForm(request.form)
    if request.method == 'POST':
        image = images.save(request.files['favicon_image'])
        favicon_image = AppleTouchIcon(image=image)
        db.session.add(favicon_image)
        db.session.commit()
        flash("Favicon Added Successfully .", "success")
        return redirect(url_for('content_manager.added_apple_touch_icon'))
    return render_template('content_manager/apple_touch_icon/add_apple_touch_icon.html', form=form)

# Favicon Image Delete Method 
@content_manager.route('/apple_touch_icon/delete/<int:apple_touch_icon_id>', methods=['POST', 'GET'])
@login_required
def delete_apple_touch_icon(apple_touch_icon_id):
    apple_touch_icon_data = AppleTouchIcon.query.get(apple_touch_icon_id)
    db.session.delete(apple_touch_icon_data)
    db.session.commit()
    flash("Image Deleted Successfully.", "success")
    return redirect(url_for('content_manager.added_apple_touch_icon'))


@content_manager.route('/trackingscript-list')
@login_required
def added_trackingscript():
    """View added tracking script."""
    data = TrackingScript.query.all()
    if data is None:
        return redirect(url_for('content_manager.add_trackingscript'))
    return render_template(
        'content_manager/trackingscript/added_trackingscript.html', data=data)

# Add TrackingScript 
@content_manager.route('/trackingscript/add', methods=['POST', 'GET'])
@login_required
def add_trackingscript():
    form = TrackingScriptForm()
    if form.validate_on_submit():
        data = TrackingScript(
            name=form.name.data,
            script=form.script.data
            )
        db.session.add(data)
        db.session.commit()
        flash("Tracking Script Added Successfully.", "success")
        return redirect(url_for('content_manager.added_trackingscript'))
    return render_template('content_manager/trackingscript/add_trackingscript.html', form=form)


# Edit SEO 
@content_manager.route('/trackingscript/<int:id>/edit', methods=['POST', 'GET'])
@login_required
def edit_trackingscript(id):
    data = TrackingScript.query.filter_by(id=id).first()
    form = TrackingScriptForm(obj=data)
    if form.validate_on_submit():
        data.name=form.name.data
        data.script=form.script.data
        db.session.add(data)
        db.session.commit()
        flash("Edit successfully.", "success")
        return redirect(url_for('content_manager.added_trackingscript'))
    else:
        flash('ERROR! Text was not edited.', 'error')
    return render_template('content_manager/trackingscript/add_trackingscript.html', form=form)

@content_manager.route('/trackingscript/<int:id>/_delete', methods=['GET', 'POST'])
@login_required
def delete_trackingscript(id):
    """Delete the item """
    data = TrackingScript.query.filter_by(id=id).first()
    db.session.commit()
    db.session.delete(data)
    flash('Successfully deleted ' , 'success')
    return redirect(url_for('content_manager.added_trackingscript'))




# Add Location 
@content_manager.route('/location/add', methods=['POST', 'GET'])
@login_required
def add_location():
    form = LocationForm()
    if form.validate_on_submit():
        data = Location(
            locality=form.locality.data,
            town=form.town.data
            )
        db.session.add(data)
        db.session.commit()
        flash("Location Added Successfully.", "success")
        return redirect(url_for('content_manager.added_location'))
    return render_template('content_manager/location/add_location.html', form=form)


@content_manager.route('/location')
@login_required
def added_location():
    """View added location."""
    data = Location.query.all()
    if data is None:
        return redirect(url_for('content_manager.add_location'))
    return render_template(
        'content_manager/location/added_location.html', data=data)

# Edit Location 
@content_manager.route('/location/<int:id>/edit', methods=['POST', 'GET'])
@login_required

def edit_location(id):
    data = Location.query.filter_by(id=id).first()
    form = LocationForm(obj=data)
    if form.validate_on_submit():
        data.town=form.town.data
        data.locality=form.locality.data
        db.session.add(data)
        db.session.commit()
        flash("Edit successfully.", "success")
        return redirect(url_for('content_manager.added_location'))
    else:
        flash('ERROR! Text was not edited.', 'error')
    return render_template('content_manager/location/add_location.html', form=form)

@content_manager.route('/location/<int:id>/_delete', methods=['GET', 'POST'])
@login_required
def delete_location(id):
    """Delete the item """
    data = Location.query.filter_by(id=id).first()
    db.session.commit()
    db.session.delete(data)
    flash('Successfully deleted ' , 'success')
    return redirect(url_for('content_manager.added_location'))



# Add Pricing
@content_manager.route('/pricing/setting', methods=['POST', 'GET'])
@login_required
def added_pricing():
    """View added Pricing setting."""
    data = Pricing.query.all()
    #cost_data = Cost.query.all()
    pricing_attributes = PricingAttribute.query.all()
    if data is None:
        return redirect(url_for('content_manager.add_pricing'))
    return render_template(
        'content_manager/pricing/added_pricing.html', data=data)#, cost_data = Cost.query.all(),
        #pricing_attributes = PricingAttribute.query.all())

@content_manager.route('/pricing/setting/add', methods=['POST', 'GET'])
@login_required
def add_pricing():
    form = PricingForm()
    if form.validate_on_submit():
        data = Pricing(
            title = form.title.data,
            description = form.description.data,
            button_text=form.button_text.data,
            button_url=form.button_url.data,
            button_type=form.button_type.data,
            is_popular=form.is_popular.data
            )
        db.session.add(data)
        db.session.commit()
        flash("Settings Added Successfully.", "success")
        return redirect(url_for('content_manager.added_pricing'))
    return render_template('content_manager/pricing/add_pricing.html', form=form)


# Edit Pricing
@content_manager.route('/pricing/<int:id>/edit', methods=['POST', 'GET'])
@login_required
def edit_pricing(id):
    data = Pricing.query.filter_by(id=id).first()
    form = PricingForm(obj=data)
    if form.validate_on_submit():
        data.title=form.title.data
        data.button_text=form.button_text.data
        data.button_url=form.button_url.data
        data.button_type=form.button_type.data
        data.is_popular=form.is_popular.data
        data.description=form.description.data
        db.session.add(data)
        db.session.commit()
        flash("Pricing Added Successfully.", "success")
        return redirect(url_for('content_manager.added_pricing'))
    else:
        flash('ERROR! Pricing was not edited.', 'error')
    return render_template('content_manager/pricing/add_pricing.html', form=form)

@content_manager.route('/pricing/setting/<int:id>/_delete', methods=['GET', 'POST'])
@login_required
def delete_pricing(id):
    """Delete the link html added """
    data = Pricing.query.filter_by(id=id).first()
    db.session.commit()
    db.session.delete(data)
    flash('Successfully deleted ' , 'success')
    if data is None:
        return redirect(url_for('content_manager.add_pricing'))
    return redirect(url_for('content_manager.added_pricing'))

#Add Pricing Attribute
@content_manager.route('/pricing/<title>/feature/<int:id>/add', methods=['POST', 'GET'])
@login_required
def add_pricing_attribute(id, title):
    pricing_id = Pricing.query.filter_by(id=id).first()
    form = PricingAttributeForm()
    if form.validate_on_submit():
        data = PricingAttribute(
            description = form.description.data,
            is_available = form.is_available.data,
            pricing_id=id
            )
        db.session.add(data)
        db.session.commit()
        flash("Settings Added Successfully.", "success")
        return redirect(url_for('content_manager.added_pricing_attribute', id=pricing_id.id, title=pricing_id.title))
    return render_template('content_manager/pricing/add_pricing_attribute.html', form=form)

@content_manager.route('/pricing/<title>/<int:id>/', methods=['POST', 'GET'])
@login_required
def added_pricing_attribute(id, title):
    """View added Pricing Attribute setting."""
    data = PricingAttribute.query.filter_by(pricing_id=id).all()
    pricing_data = PricingAttribute.query.filter_by(pricing_id=id).first()
    if data is None:
        return redirect(url_for('content_manager.add_pricing_attribute', id=id))
    return render_template(
        'content_manager/pricing/added_pricing_attribute.html', data=data, title=title, id=id, pricing_data = pricing_data)


# Edit PricingAttribute
@content_manager.route('/pricing_attribute/<int:id>/edit', methods=['POST', 'GET'])
@login_required
def edit_pricing_attribute(id):
    pricing_id = Pricing.query.filter_by(id=id).first()
    data = PricingAttribute.query.filter_by(id=id).first()
    form = PricingAttributeForm(obj=data)
    if form.validate_on_submit():
        data.description=form.description.data
        data.is_available=form.is_available.data
        db.session.add(data)
        db.session.commit()
        flash("PricingAttribute Added Successfully.", "success")
        return redirect(url_for('content_manager.added_pricing_attribute', id=id, title=pricing_id.title))
    else:
        flash('ERROR! PricingAttribute was not edited.', 'error')
    return render_template('content_manager/pricing/add_pricing_attribute.html', form=form)

@content_manager.route('/pricing_attribute/setting/<int:id>/_delete', methods=['GET', 'POST'])
@login_required
def delete_pricing_attribute(id):
    """Delete the pricing attribute added """
    data = PricingAttribute.query.filter_by(id=id).first()
    db.session.commit()
    db.session.delete(data)
    flash('Successfully deleted ' , 'success')
    if data is None:
        return redirect(url_for('content_manager.add_pricing_attribute'))
    return redirect(url_for('content_manager.added_pricing_attribute'))

# Add Cost
@content_manager.route('/cost/<int:id>/<title>', methods=['POST', 'GET'])
@login_required
def added_cost(id, title):
    """View added Cost setting."""
    data = Cost.query.filter_by(pricing_id=id).first()
    if data is None:
        return redirect(url_for('content_manager.add_cost', id=id))
    return render_template(
        'content_manager/pricing/added_cost.html', data=data, title=title)

@content_manager.route('/cost/<int:id>/add', methods=['POST', 'GET'])
@login_required
def add_cost(id):
    pricing_id = Pricing.query.filter_by(id=id).first()
    cost_exist = Cost.query.filter_by(pricing_id=id).first()
    if cost_exist is not None:
        return redirect(url_for('content_manager.added_cost', id=id, title=pricing_id.title))
    form = CostForm()
    if form.validate_on_submit():
        data = Cost(
            figure = form.figure.data,
           currency = form.currency.data,
           currency_icon = form.currency_icon.data,
            pricing_id=id
            )
        db.session.add(data)
        db.session.commit()
        flash("Settings Added Successfully.", "success")
        return redirect(url_for('content_manager.added_cost', id=id, title=pricing_id.title))
    return render_template('content_manager/pricing/add_cost.html', form=form)


# Edit Cost
@content_manager.route('/cost/<int:id>/edit', methods=['POST', 'GET'])
@login_required
def edit_cost(id):
    data = Cost.query.filter_by(id=id).first()
    form = CostForm(obj=data)
    if form.validate_on_submit():
        data.currency=form.currency.data
        data.currency_icon=form.currency_ico.data
        data.figure=form.figure.data
        db.session.add(data)
        db.session.commit()
        flash("Cost Added Successfully.", "success")
        return redirect(url_for('content_manager.added_cost'))
    else:
        flash('ERROR! Cost was not edited.', 'error')
    return render_template('content_manager/pricing/add_cost.html', form=form)

@content_manager.route('/cost/setting/<int:id>/_delete', methods=['GET', 'POST'])
@login_required
def delete_cost(id):
    """Delete the link html added """
    data = Cost.query.filter_by(id=id).first()
    db.session.commit()
    db.session.delete(data)
    flash('Successfully deleted ' , 'success')
    if data is None:
        return redirect(url_for('content_manager.add_cost'))
    return redirect(url_for('content_manager.added_cost'))

# Added PricingTitle Area
@content_manager.route('/pricing_title')
@login_required
def added_pricing_title():
    """View added pricing_title and description."""
    data = PricingTitle.query.first()
    if data is None:
        return redirect(url_for('content_manager.add_pricing_title'))
    return render_template(
        'content_manager/pricing_title/added_pricing_title.html', data=data)

# Add PricingTitle Area
@content_manager.route('/pricing_title/add', methods=['POST', 'GET'])
@login_required
def add_pricing_title():
    form = PricingTitleForm()
    if form.validate_on_submit():
        data = PricingTitle(
            description=form.description.data
            )
        db.session.add(data)
        db.session.commit()
        flash("Added Successfully.", "success")
        return redirect(url_for('content_manager.added_pricing_title'))
    return render_template('content_manager/pricing_title/add_pricing_title.html', form=form)

# Edit PricingTitle Area
@content_manager.route('/pricing_title/<int:id>/edit', methods=['POST', 'GET'])
@login_required
def edit_pricing_title(id):
    data = PricingTitle.query.filter_by(id=id).first()
    form = PricingTitleForm(obj=data)
    if form.validate_on_submit():
        data.description=form.description.data
        db.session.add(data)
        db.session.commit()
        flash("Edited Successfully.", "success")
        return redirect(url_for('content_manager.added_pricing_title'))
    else:
        flash('ERROR! Data was not edited.', 'error')
    return render_template('content_manager/pricing_title/add_pricing_title.html', form=form)

@content_manager.route('/pricing_title/<int:id>/_delete', methods=['GET', 'POST'])
@login_required
def delete_pricing_title(id):
    """Delete the item """
    data = PricingTitle.query.filter_by(id=id).first()
    db.session.commit()
    db.session.delete(data)
    flash('Successfully deleted ' , 'success')
    return redirect(url_for('content_manager.added_pricing_title'))

# Added Process Steps
@content_manager.route('/process')
@login_required
def added_process():
    """View added process steps."""
    data = Process.query.all()
    if data is None:
        return redirect(url_for('content_manager.add_process'))
    return render_template(
        'content_manager/process/added_process.html', data=data)

# Add Process 
@content_manager.route('/process/add', methods=['POST', 'GET'])
@login_required
def add_process():
    form = ProcessForm()
    if form.validate_on_submit():
        data = Process(
            steps=form.steps.data,
            description=form.description.data,
            #process_icon = form.process_icon.data
            )
        db.session.add(data)
        db.session.commit()
        flash("Added Successfully.", "success")
        return redirect(url_for('content_manager.added_process'))
    return render_template('content_manager/process/add_process.html', form=form)

# Edit Process
@content_manager.route('/process/<int:id>/edit', methods=['POST', 'GET'])
@login_required

def edit_process(id):
    data = Process.query.filter_by(id=id).first()
    form = ProcessForm(obj=data)
    if form.validate_on_submit():
        data.steps=form.steps.data,
        data.description=form.description.data,
        #data.process_icon = form.process_icon.data,
        data.description=form.description.data
        db.session.add(data)
        db.session.commit()
        flash("Edited Successfully.", "success")
        return redirect(url_for('content_manager.added_process'))
    else:
        flash('ERROR! Data was not edited.', 'error')
    return render_template('content_manager/process/add_process.html', form=form)

@content_manager.route('/process/<int:id>/_delete', methods=['GET', 'POST'])
@login_required
def delete_process(id):
    """Delete the item """
    data = Process.query.filter_by(id=id).first()
    db.session.commit()
    db.session.delete(data)
    flash('Successfully deleted ' , 'success')
    return redirect(url_for('content_manager.added_process'))


# Added ProcessTitle Steps
@content_manager.route('/process_title')
@login_required
def added_process_title():
    """View added process_title and description."""
    data = ProcessTitle.query.first()
    if data is None:
        return redirect(url_for('content_manager.add_process_title'))
    return render_template(
        'content_manager/process_title/added_process_title.html', data=data)

# Add ProcessTitle Area
@content_manager.route('/process_title/add', methods=['POST', 'GET'])
@login_required
def add_process_title():
    form = ProcessTitleForm()
    if form.validate_on_submit():
        data = ProcessTitle(
            title=form.title.data,
            description=form.description.data,
            image = images.save(request.files['image'])
            )
        db.session.add(data)
        db.session.commit()
        flash("Added Successfully.", "success")
        return redirect(url_for('content_manager.added_process_title'))
    return render_template('content_manager/process_title/add_process_title.html', form=form)

# Edit ProcessTitle Area
@content_manager.route('/process_title/<int:id>/edit', methods=['POST', 'GET'])
@login_required

def edit_process_title(id):
    data = ProcessTitle.query.filter_by(id=id).first()
    form = ProcessTitleForm(obj=data)
    if form.validate_on_submit():
        data.title=form.title.data
        data.description=form.description.data
        data.image=images.save(request.files['image'])
        db.session.add(data)
        db.session.commit()
        flash("Edited Successfully.", "success")
        return redirect(url_for('content_manager.added_process_title'))
    else:
        flash('ERROR! Data was not edited.', 'error')
    return render_template('content_manager/process_title/add_process_title.html', form=form)

@content_manager.route('/process_title/<int:id>/_delete', methods=['GET', 'POST'])
@login_required
def delete_process_title(id):
    """Delete the item """
    data = ProcessTitle.query.filter_by(id=id).first()
    db.session.commit()
    db.session.delete(data)
    flash('Successfully deleted ' , 'success')
    return redirect(url_for('content_manager.added_process_title'))

# Added ClientTitle Steps
@content_manager.route('/client_title')
@login_required
def added_client_title():
    """View added client_title and description."""
    data = ClientTitle.query.first()
    if data is None:
        return redirect(url_for('content_manager.add_client_title'))
    return render_template(
        'content_manager/client_title/added_client_title.html', data=data)

# Add ClientTitle 
@content_manager.route('/client_title/add', methods=['POST', 'GET'])
@login_required
def add_client_title():
    form = ClientTitleForm()
    if form.validate_on_submit():
        data = ClientTitle(
            title=form.title.data,
            description=form.description.data
            )
        db.session.add(data)
        db.session.commit()
        flash("Added Successfully.", "success")
        return redirect(url_for('content_manager.added_client_title'))
    return render_template('content_manager/client_title/add_client_title.html', form=form)

# Edit ClientTitle
@content_manager.route('/client_title/<int:id>/edit', methods=['POST', 'GET'])
@login_required

def edit_client_title(id):
    data = ClientTitle.query.filter_by(id=id).first()
    form = ClientTitleForm(obj=data)
    if form.validate_on_submit():
        data.title=form.title.data
        data.description=form.description.data
        db.session.add(data)
        db.session.commit()
        flash("Edited Successfully.", "success")
        return redirect(url_for('content_manager.added_client_title'))
    else:
        flash('ERROR! Data was not edited.', 'error')
    return render_template('content_manager/client_title/add_client_title.html', form=form)

@content_manager.route('/client_title/<int:id>/_delete', methods=['GET', 'POST'])
@login_required
def delete_client_title(id):
    """Delete the item """
    data = ClientTitle.query.filter_by(id=id).first()
    db.session.commit()
    db.session.delete(data)
    flash('Successfully deleted ' , 'success')
    return redirect(url_for('content_manager.added_client_title'))


# Added TestimonialTitle Area
@content_manager.route('/testimonial_title')
@login_required
def added_testimonial_title():
    """View added testimonial_title and description."""
    data = TestimonialTitle.query.first()
    if data is None:
        return redirect(url_for('content_manager.add_testimonial_title'))
    return render_template(
        'content_manager/testimonial_title/added_testimonial_title.html', data=data)

# Add TestimonialTitle Area
@content_manager.route('/testimonial_title/add', methods=['POST', 'GET'])
@login_required
def add_testimonial_title():
    form = TestimonialTitleForm()
    if form.validate_on_submit():
        data = TestimonialTitle(
            description=form.description.data,
            title=form.title.data
            )
        db.session.add(data)
        db.session.commit()
        flash("Added Successfully.", "success")
        return redirect(url_for('content_manager.added_testimonial_title'))
    return render_template('content_manager/testimonial_title/add_testimonial_title.html', form=form)

# Edit TestimonialTitle Area
@content_manager.route('/testimonial_title/<int:id>/edit', methods=['POST', 'GET'])
@login_required
def edit_testimonial_title(id):
    data = TestimonialTitle.query.filter_by(id=id).first()
    form = TestimonialTitleForm(obj=data)
    if form.validate_on_submit():
        data.description=form.description.data
        data.title=form.title.data
        db.session.add(data)
        db.session.commit()
        flash("Edited Successfully.", "success")
        return redirect(url_for('content_manager.added_testimonial_title'))
    else:
        flash('ERROR! Data was not edited.', 'error')
    return render_template('content_manager/testimonial_title/add_testimonial_title.html', form=form)

@content_manager.route('/testimonial_title/<int:id>/_delete', methods=['GET', 'POST'])
@login_required
def delete_testimonial_title(id):
    """Delete the item """
    data = TestimonialTitle.query.filter_by(id=id).first()
    db.session.commit()
    db.session.delete(data)
    flash('Successfully deleted ' , 'success')
    return redirect(url_for('content_manager.added_testimonial_title'))




# Added FeatureTitle Area
@content_manager.route('/feature_title')
@login_required
def added_feature_title():
    """View added feature_title and description."""
    data = FeatureTitle.query.first()
    if data is None:
        return redirect(url_for('content_manager.add_feature_title'))
    return render_template(
        'content_manager/feature_title/added_feature_title.html', data=data)

# Add FeatureTitle Area
@content_manager.route('/feature_title/add', methods=['POST', 'GET'])
@login_required
def add_feature_title():
    form = FeatureTitleForm()
    if form.validate_on_submit():
        data = FeatureTitle(
            title=form.title.data,
            description=form.description.data
            )
        db.session.add(data)
        db.session.commit()
        flash("Added Successfully.", "success")
        return redirect(url_for('content_manager.added_feature_title'))
    return render_template('content_manager/feature_title/add_feature_title.html', form=form)

# Edit FeatureTitle Area
@content_manager.route('/feature_title/<int:id>/edit', methods=['POST', 'GET'])
@login_required
def edit_feature_title(id):
    data = FeatureTitle.query.filter_by(id=id).first()
    form = FeatureTitleForm(obj=data)
    if form.validate_on_submit():
        data.title=form.title.data
        data.description=form.description.data
        db.session.add(data)
        db.session.commit()
        flash("Edited Successfully.", "success")
        return redirect(url_for('content_manager.added_feature_title'))
    else:
        flash('ERROR! Data was not edited.', 'error')
    return render_template('content_manager/feature_title/add_feature_title.html', form=form)

@content_manager.route('/feature_title/<int:id>/_delete', methods=['GET', 'POST'])
@login_required
def delete_feature_title(id):
    """Delete the item """
    data = FeatureTitle.query.filter_by(id=id).first()
    db.session.commit()
    db.session.delete(data)
    flash('Successfully deleted ' , 'success')
    return redirect(url_for('content_manager.added_feature_title'))


# Added ServiceTitle Area
@content_manager.route('/service_title')
@login_required
def added_service_title():
    """View added service_title and description."""
    data = ServiceTitle.query.first()
    if data is None:
        return redirect(url_for('content_manager.add_service_title'))
    return render_template(
        'content_manager/service_title/added_service_title.html', data=data)

# Add ServiceTitle Area
@content_manager.route('/service_title/add', methods=['POST', 'GET'])
@login_required
def add_service_title():
    form = ServiceTitleForm()
    if form.validate_on_submit():
        data = ServiceTitle(
            title=form.title.data,
            description=form.description.data
            )
        db.session.add(data)
        db.session.commit()
        flash("Added Successfully.", "success")
        return redirect(url_for('content_manager.added_service_title'))
    return render_template('content_manager/service_title/add_service_title.html', form=form)

# Edit ServiceTitle Area
@content_manager.route('/service_title/<int:id>/edit', methods=['POST', 'GET'])
@login_required
def edit_service_title(id):
    data = ServiceTitle.query.filter_by(id=id).first()
    form = ServiceTitleForm(obj=data)
    if form.validate_on_submit():
        data.title=form.title.data
        data.description=form.description.data
        db.session.add(data)
        db.session.commit()
        flash("Edited Successfully.", "success")
        return redirect(url_for('content_manager.added_service_title'))
    else:
        flash('ERROR! Data was not edited.', 'error')
    return render_template('content_manager/service_title/add_service_title.html', form=form)

@content_manager.route('/service_title/<int:id>/_delete', methods=['GET', 'POST'])
@login_required
def delete_service_title(id):
    """Delete the item """
    data = ServiceTitle.query.filter_by(id=id).first()
    db.session.commit()
    db.session.delete(data)
    flash('Successfully deleted ' , 'success')
    return redirect(url_for('content_manager.added_service_title'))
