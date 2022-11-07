from flask import url_for
from wtforms.fields import Field
from wtforms.widgets import HiddenInput


def register_template_utils(app):
    """Register Jinja 2 helpers (called from __init__.py)."""

    @app.template_test()
    def equalto(value, other):
        return value == other

    @app.template_global()
    def is_hidden_field(field):
        from wtforms.fields import HiddenField
        return isinstance(field, HiddenField)

    @app.template_filter('user')
    def user(o):
        """check if object is user"""
        from app.models import User
        return o.__class__ == User

    @app.template_filter('preference')
    def preference(o):
        """check if object is user"""
        from app.models import Seeking
        return o.__class__ == Seeking

    app.add_template_global(index_for_role)


def index_for_role(role):
    return url_for(role.index)


class CustomSelectField(Field):
    widget = HiddenInput()

    def __init__(self,
                 label='',
                 validators=None,
                 multiple=False,
                 choices=[],
                 allow_custom=True,
                 **kwargs):
        super(CustomSelectField, self).__init__(label, validators, **kwargs)
        self.multiple = multiple
        self.choices = choices
        self.allow_custom = allow_custom

    def _value(self):
        return str(self.data) if self.data is not None else ''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = valuelist[1]
            self.raw_data = [valuelist[1]]
        else:
            self.data = ''
