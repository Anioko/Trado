from datetime import datetime
from math import ceil, floor

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


def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    from datetime import datetime
    now = datetime.now()

    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time, datetime):
        diff = now - time
    elif not time:
        diff = now - now
    # diff = map(int, diff)
    # diff = floor(diff)
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(ceil(second_diff)) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(floor(second_diff / 60)) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(floor(second_diff / 3600)) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        # if d
        return str(floor(day_diff)) + " days ago"
    if day_diff < 31:
        day_diff = floor(day_diff / 7)
        if day_diff == 1:
            return "a week ago"
        else:
            return str(day_diff) + " weeks ago"
    if day_diff < 365:
        return str(floor(day_diff / 30)) + " months ago"
    return str(floor(day_diff / 365)) + " years ago"


async def jsonify_object(item, only_date=True):
    item = await item
    new_item = {}
    for item_attr in item._asdict():
        if not item_attr.startswith('_'):
            value = item.__dict__[item_attr] if type(
                item.__dict__[item_attr]) is not datetime else (
                    str(item.__dict__[item_attr]) if not only_date else
                    pretty_date(item.__dict__[item_attr]))
            new_item[item_attr] = value
    return new_item


def get_paginated_list(results):
    return_value = jsonify_object(results)
    items = []
    for item in results.items:
        items.append(jsonify_object(item))
    items.reverse()
    return_value['items'] = items
    del (return_value['query'])
    return return_value
