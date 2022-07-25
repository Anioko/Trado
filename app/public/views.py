from flask import Blueprint, render_template

from app.models import EditableHTML

public = Blueprint('public', __name__)


@public.route('/')
def index():
    return render_template('public/index.html')


@public.route('/about')
def about():
    editable_html_obj = EditableHTML.get_editable_html('about')
    return render_template(
        'public/about.html', editable_html_obj=editable_html_obj)
