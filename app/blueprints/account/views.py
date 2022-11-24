from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_rq import get_queue

from app import db
from app.blueprints.account.forms import (
    ChangeUsernameForm,
    ChangeEmailForm,
    ChangePasswordForm,
    CreatePasswordForm,
    LoginForm,
    RegistrationForm,
    RequestResetPasswordForm,
    ResetPasswordForm,
    UpdateDetailsForm,
    PrivacyForm
)
from app.blueprints.seeking.forms import *
from app.email import send_email
from app.models import User, Photo, Seeking, Page

account = Blueprint('account', __name__)



@account.route('/login', methods=['GET', 'POST'])
def login():
    """Log in an existing user."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.password_hash is not None and \
                user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash('You are now logged in. Welcome back!', 'success')
            return redirect(request.args.get('next') or url_for('account.manage'))
        else:
            flash('Invalid email or password.', 'error')
    pages = Page.query.all()
    return render_template('socialite/form-login.html', form=form, pages=pages)



@account.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new user, and send them a confirmation email."""
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            height = form.height.data,
            sex = form.sex.data,
            age = form.age.data,
            city = form.city.data,
            state = form.state.data,
            country = form.country.data,
            religion = form.religion.data,
            ethnicity = form.ethnicity.data, 
            marital_type = form.marital_type.data,
            body_type = form.body_type.data,
            church_denomination = form.church_denomination.data,
            current_status = form.current_status.data,
            drinking_status = form.drinking_status.data, 
            smoking_status = form.smoking_status.data,
            education_level = form.education_level.data, 
            has_children = form.has_children.data,
            want_children = form.want_children.data,
            open_for_relocation = form.open_for_relocation.data,
            
            password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        confirm_link = url_for('account.confirm', token=token, _external=True)
        get_queue().enqueue(
            send_email,
            recipient=user.email,
            subject='Confirm Your Account',
            template='account/email/confirm',
            user=user,
            confirm_link=confirm_link)
        flash('A confirmation link has been sent to {}.'.format(user.email),
              'warning')
        return redirect(url_for('account.manage'))
    pages = Page.query.all()
    return render_template('socialite/form-register.html', form=form, pages=pages)




@account.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('account.manage'))


@account.route('/manage', methods=['GET', 'POST'])
@account.route('/manage/info', methods=['GET', 'POST'])
@login_required
def manage():
    """Display a user's account information."""
    data = Photo.query.filter_by(user_id=current_user.id, profile_picture=True).first()
    """Change an existing user's password."""
    change_password_form = ChangePasswordForm()
    if change_password_form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = change_password_form.new_password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.', 'form-success')
            return redirect(url_for('account.manage'))
        else:
            flash('Original password is invalid.', 'form-error')
            
    """ Update privacy """
    user = User.query.filter_by(id=current_user.id).first()
    privacy_form = PrivacyForm(obj=user)
    if privacy_form.validate_on_submit():
        user.is_public = privacy_form.is_public.data
        user.hide_profile = privacy_form.hide_profile.data
        db.session.add(user)
        db.session.commit()
        flash("Edited Successfully.", "success")
        return redirect(url_for('account.manage'))
    else:
        flash('Invalid data.', 'form-error')
        
    """ Change a username """
    change_username_form = ChangeUsernameForm(obj=current_user)
    if change_username_form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            current_user.username = change_username_form.username.data
            flash('New username changed to {}.'.format(user.username),
                  'success')
            return redirect(url_for('account.manage'))
        else:
            flash('Invalid email or password.', 'form-error')

    """Respond to existing user's request to change their email."""
    change_email_form = ChangeEmailForm()
    if change_email_form.validate_on_submit():
        if current_user.verify_password(change_email_form.password.data):
            new_email = change_email_form.email.data
            token = current_user.generate_email_change_token(new_email)
            change_email_link = url_for(
                'account.change_email', token=token, _external=True)
            get_queue().enqueue(
                send_email,
                recipient=new_email,
                subject='Confirm Your New Email',
                template='account/email/change_email',
                # current_user is a LocalProxy, we want the underlying user
                # object
                user=current_user._get_current_object(),
                change_email_link=change_email_link)
            flash('A confirmation link has been sent to {}.'.format(new_email),
                  'warning')
            return redirect(url_for('account.manage'))
        else:
            flash('Invalid email or password.', 'form-error')
            
    user = User.query.filter_by(id=current_user.id).first()
    update_details_form = UpdateDetailsForm(obj=user)
    if update_details_form.validate_on_submit():
        user.first_name=update_details_form.first_name.data
        user.last_name=update_details_form.last_name.data
        user.height = update_details_form.height.data
        user.sex = update_details_form.sex.data
        user.looking_for = update_details_form.looking_for.data
        user.age = update_details_form.age.data
        user.city = update_details_form.city.data
        user.state = update_details_form.state.data
        user.country = update_details_form.country.data
        user.religion = update_details_form.religion.data
        user.ethnicity = update_details_form.ethnicity.data
        user.marital_type = update_details_form.marital_type.data
        user.body_type = update_details_form.body_type.data
        user.church_denomination = update_details_form.church_denomination.data
        user.current_status = update_details_form.current_status.data
        user.drinking_status = update_details_form.drinking_status.data 
        user.smoking_status = update_details_form.smoking_status.data
        user.education_level = update_details_form.education_level.data 
        user.has_children = update_details_form.has_children.data
        user.want_children = update_details_form.want_children.data
        user.open_for_relocation = update_details_form.open_for_relocation.data
        db.session.add(user)
        db.session.commit()
        flash("Edited Successfully.", "success")
        return redirect(url_for('account.manage'))
    else:
        flash('Invalid data.', 'form-error')

    seeking_form = SeekingForm()
    if seeking_form.validate_on_submit():
        seeking = Seeking(
            
            user_id = current_user.id,
            
            seeking_partner = seeking_form.seeking_partner.data,
            seeking_from_height = seeking_form.seeking_from_height.data,
            seeking_to_height = seeking_form.seeking_to_height.data,
            seeking_sex = seeking_form.seeking_sex.data,
            
            seeking_from_age = seeking_form.seeking_from_age.data,
            seeking_to_age = seeking_form.seeking_to_age.data,
            
            seeking_country_one = seeking_form.seeking_country_one.data,
            seeking_country_two = seeking_form.seeking_country_two.data,
            seeking_country_three = seeking_form.seeking_country_three.data,
            seeking_country_four = seeking_form.seeking_country_four.data,
            seeking_country_five = seeking_form.seeking_country_five.data,
            seeking_country_six = seeking_form.seeking_country_six.data,
            seeking_country_seven = seeking_form.seeking_country_seven.data,
            seeking_country_eight = seeking_form.seeking_country_eight.data,
            
            seeking_religion_one = seeking_form.seeking_religion_one.data,
            seeking_religion_two = seeking_form.seeking_religion_two.data,
            seeking_religion_three = seeking_form.seeking_religion_three.data,
            
            seeking_ethnicity_one = seeking_form.seeking_ethnicity_one.data,
            seeking_ethnicity_two = seeking_form.seeking_ethnicity_two.data,
            seeking_ethnicity_three = seeking_form.seeking_ethnicity_three.data,
            seeking_ethnicity_four = seeking_form.seeking_ethnicity_four.data,
            seeking_ethnicity_five = seeking_form.seeking_ethnicity_five.data,
            
            seeking_marital_type_one = seeking_form.seeking_marital_type_one.data,
            
            seeking_body_type_one = seeking_form.seeking_body_type_one.data,
            seeking_body_type_two = seeking_form.seeking_body_type_two.data,
            seeking_body_type_three = seeking_form.seeking_body_type_three.data,
            seeking_body_type_four = seeking_form.seeking_body_type_four.data,
            
            seeking_church_denomination_one = seeking_form.seeking_church_denomination_one.data,
            seeking_church_denomination_two = seeking_form.seeking_church_denomination_two.data,
            seeking_church_denomination_three = seeking_form.seeking_church_denomination_three.data,
            seeking_church_denomination_four = seeking_form.seeking_church_denomination_four.data,
            seeking_church_denomination_five = seeking_form.seeking_church_denomination_five.data,
            seeking_church_denomination_six = seeking_form.seeking_church_denomination_six.data,

            seeking_current_status_one = seeking_form.seeking_current_status_one.data,
            seeking_current_status_two = seeking_form.seeking_current_status_two.data,
            seeking_current_status_three = seeking_form.seeking_current_status_three.data,
            
            seeking_drinking_status_one = seeking_form.seeking_drinking_status_one.data,
            seeking_drinking_status_two = seeking_form.seeking_drinking_status_two.data,
            
            seeking_smoking_status_one = seeking_form.seeking_smoking_status_one.data,
            seeking_smoking_status_two = seeking_form.seeking_smoking_status_two.data,
            
            seeking_education_level_one = seeking_form.seeking_education_level_one.data,
            seeking_education_level_two = seeking_form.seeking_education_level_two.data,
            seeking_education_level_three = seeking_form.seeking_education_level_three.data,
            seeking_education_level_four = seeking_form.seeking_education_level_four.data,
            seeking_education_level_five = seeking_form.seeking_education_level_five.data,
            seeking_education_level_six = seeking_form.seeking_education_level_six.data,
            seeking_education_level_seven = seeking_form.seeking_education_level_seven.data,
            seeking_education_level_eight = seeking_form.seeking_education_level_eight.data,
            seeking_education_level_nine = seeking_form.seeking_education_level_nine.data,
            
            seeking_has_children_one = seeking_form.seeking_has_children_one.data,
            seeking_has_children_two = seeking_form.seeking_has_children_two.data,
            seeking_has_children_three = seeking_form.seeking_has_children_three.data,
            
            seeking_want_children_one = seeking_form.seeking_want_children_one.data,
            seeking_want_children_two = seeking_form.seeking_want_children_two.data,
            seeking_want_children_three = seeking_form.seeking_want_children_three.data,
            
            
            seeking_open_for_relocation = seeking_form.seeking_open_for_relocation.data
                        )
        db.session.add(seeking)
        db.session.commit()
        flash('You have successfully added details on what you are looking for',
              'success')
    
    pages = Page.query.all()
    return render_template('socialite/pages-setting.html', user=current_user, form=None, data=data,
                           change_password_form=change_password_form,
                           change_username_form=change_username_form,
                           change_email_form=change_email_form,
                           update_details_form=update_details_form,
                           privacy_form=privacy_form, pages=pages,
                           seeking_form=seeking_form)




@account.route('/profile', methods=['GET', 'POST'])
@account.route('/profile/info', methods=['GET', 'POST'])
@login_required
def profile():
    """Display a user's profile."""
    profile_picture = Photo.query.filter_by(user_id=current_user.id, profile_picture=True).first()
    photo_data = Photo.query.filter_by(user_id=current_user.id).all()
    preferences_data = Seeking.query.filter_by(user_id=current_user.id).first()
    return render_template('account/profile.html', user=current_user, photo_data=photo_data, preferences_data=preferences_data,
                           profile_picture=profile_picture)


@account.route('/reset-password', methods=['GET', 'POST'])
def reset_password_request():
    """Respond to existing user's request to reset their password."""
    if not current_user.is_anonymous:
        return redirect(url_for('account.manage'))
    form = RequestResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_password_reset_token()
            reset_link = url_for(
                'account.reset_password', token=token, _external=True)
            get_queue().enqueue(
                send_email,
                recipient=user.email,
                subject='Reset Your Password',
                template='account/email/reset_password',
                user=user,
                reset_link=reset_link,
                next=request.args.get('next'))
        flash('A password reset link has been sent to {}.'.format(
            form.email.data), 'warning')
        return redirect(url_for('account.login'))
    return render_template('account/reset_password.html', form=form)


@account.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset an existing user's password."""
    if not current_user.is_anonymous:
        return redirect(url_for('account.manage'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash('Invalid email address.', 'form-error')
            return redirect(url_for('account.manage'))
        if user.reset_password(token, form.new_password.data):
            flash('Your password has been updated.', 'form-success')
            return redirect(url_for('account.login'))
        else:
            flash('The password reset link is invalid or has expired.',
                  'form-error')
            return redirect(url_for('account.manage'))
    return render_template('account/reset_password.html', form=form)


@account.route('/manage/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change an existing user's password."""
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.new_password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.', 'form-success')
            return redirect(url_for('account.manage'))
        else:
            flash('Original password is invalid.', 'form-error')
    return render_template('account/manage.html', form=form)


@account.route('/manage/change-username', methods=['GET', 'POST'])
@login_required
def change_username_request():
    """Respond to existing user's request to change their username."""
    user = User.query.filter_by(id=current_user.id).first()
    form = ChangeUsernameForm(obj=user)
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            user.username = form.username.data
            flash('New username changed to {}.'.format(user.username),
                  'success')
            return redirect(url_for('account.manage'))
        else:
            flash('Invalid email or password.', 'form-error')
    return render_template('account/manage.html', form=form)

@account.route('/manage/update-details', methods=['GET', 'POST'])
@login_required
def update_details():
    """Respond to existing user's request to update some account details."""
    user = User.query.filter_by(id=current_user.id).first()
    form = UpdateDetailsForm(obj=user)
    if form.validate_on_submit():
        user.first_name=form.first_name.data
        user.last_name=form.last_name.data
        user.height = form.height.data
        user.sex = form.sex.data
        user.age = form.age.data
        user.state = form.state.data
        user.country = form.country.data
        user.religion = form.religion.data
        user.ethnicity = form.ethnicity.data
        user.marital_type = form.marital_type.data
        user.body_type = form.body_type.data
        user.church_denomination = form.church_denomination.data
        user.current_status = form.current_status.data
        user.drinking_status = form.drinking_status.data 
        user.smoking_status = form.smoking_status.data
        user.education_level = form.education_level.data 
        user.has_children = form.has_children.data
        user.want_children = form.want_children.data
        user.open_for_relocation = form.open_for_relocation.data
        db.session.add(user)
        db.session.commit()
        flash("Edited Successfully.", "success")
        return redirect(url_for('account.manage'))
    else:
        flash('Invalid data.', 'form-error')
    return render_template('account/manage.html', form=form)

@account.route('/manage/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    """Respond to existing user's request to change their email."""
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            change_email_link = url_for(
                'account.change_email', token=token, _external=True)
            get_queue().enqueue(
                send_email,
                recipient=new_email,
                subject='Confirm Your New Email',
                template='account/email/change_email',
                # current_user is a LocalProxy, we want the underlying user
                # object
                user=current_user._get_current_object(),
                change_email_link=change_email_link)
            flash('A confirmation link has been sent to {}.'.format(new_email),
                  'warning')
            return redirect(url_for('account.manage'))
        else:
            flash('Invalid email or password.', 'form-error')
    return render_template('account/manage.html', form=form)


@account.route('/manage/change-email/<token>', methods=['GET', 'POST'])
@login_required
def change_email(token):
    """Change existing user's email with provided token."""
    if current_user.change_email(token):
        flash('Your email address has been updated.', 'success')
    else:
        flash('The confirmation link is invalid or has expired.', 'error')
    return redirect(url_for('account.manage'))


@account.route('/confirm-account')
@login_required
def confirm_request():
    """Respond to new user's request to confirm their account."""
    token = current_user.generate_confirmation_token()
    confirm_link = url_for('account.confirm', token=token, _external=True)
    get_queue().enqueue(
        send_email,
        recipient=current_user.email,
        subject='Confirm Your Account',
        template='account/email/confirm',
        # current_user is a LocalProxy, we want the underlying user object
        user=current_user._get_current_object(),
        confirm_link=confirm_link)
    flash('A new confirmation link has been sent to {}.'.format(
        current_user.email), 'warning')
    return redirect(url_for('account.manage'))


@account.route('/confirm-account/<token>')
@login_required
def confirm(token):
    """Confirm new user's account with provided token."""
    if current_user.confirmed:
        return redirect(url_for('account.manage'))
    if current_user.confirm_account(token):
        flash('Your account has been confirmed.', 'success')
    else:
        flash('The confirmation link is invalid or has expired.', 'error')
    return redirect(url_for('account.manage'))


@account.route(
    '/join-from-invite/<int:user_id>/<token>', methods=['GET', 'POST'])
def join_from_invite(user_id, token):
    """
    Confirm new user's account with provided token and prompt them to set
    a password.
    """
    if current_user is not None and current_user.is_authenticated:
        flash('You are already logged in.', 'error')
        return redirect(url_for('account.manage'))

    new_user = User.query.get(user_id)
    if new_user is None:
        return redirect(404)

    if new_user.password_hash is not None:
        flash('You have already joined.', 'error')
        return redirect(url_for('account.manage'))

    if new_user.confirm_account(token):
        form = CreatePasswordForm()
        if form.validate_on_submit():
            new_user.password = form.password.data
            db.session.add(new_user)
            db.session.commit()
            flash('Your password has been set. After you log in, you can '
                  'go to the "Your Account" page to review your account '
                  'information and settings.', 'success')
            return redirect(url_for('account.login'))
        return render_template('account/join_invite.html', form=form)
    else:
        flash('The confirmation link is invalid or has expired. Another '
              'invite email with a new link has been sent to you.', 'error')
        token = new_user.generate_confirmation_token()
        invite_link = url_for(
            'account.join_from_invite',
            user_id=user_id,
            token=token,
            _external=True)
        get_queue().enqueue(
            send_email,
            recipient=new_user.email,
            subject='You Are Invited To Join',
            template='account/email/invite',
            user=new_user,
            invite_link=invite_link)
    return redirect(url_for('account.manage'))


@account.before_app_request
def before_request():
    """Force user to confirm email before accessing login-required routes."""
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint[:8] != 'account.' \
            and request.endpoint != 'static':
        return redirect(url_for('account.unconfirmed'))


@account.route('/unconfirmed')
def unconfirmed():
    """Catch users with unconfirmed emails."""
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('account.manage'))
    return render_template('account/unconfirmed.html')
