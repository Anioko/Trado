import os

from flask import url_for
from .. import db


class Page(db.Model):
    __tablename__ = "page"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    #seo_title = db.Column(db.String(180), nullable=True)
    #seo_description = db.Column(db.String(250), nullable=True)
    content = db.Column(db.Text)
    sub_pages = db.relationship('SubPage', backref='page', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    #user = db.relationship("Page", back_populates="pages")

def page_serializer(page):
    return {
        'id':page.id,
        'name': page.name ,
        'content': page.content,
        'sub_pages': page.sub_pages,
        'user_id': page.user_id,
        'user': page.user,
        }

# Model to create sub pages under many relationships of the a page.
class SubPage(db.Model):
    __tablename__ = "sub_page"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    content = db.Column(db.Text)
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'),
        nullable=False)
    main_page_name = db.Column(db.String(50), nullable=True)

def sub_page_serializer(sub_page):
    return {
        'id':sub_page.id,
        'name': sub_page.name ,
        'content': sub_page.content,
        'page_id': sub_page.page_id,
        'main_page_name': sub_page.main_page_name,        
        }
