#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# *************************************************************************
#   Copyright © 2015 JiangLin. All rights reserved.
#   File Name: models.py
#   Author:JiangLin
#   Mail:xiyang0807@gmail.com
#   Created Time: 2015-11-08 06:42:40
# *************************************************************************
from flask import current_app
from maple import db
from datetime import datetime

tag_blog = db.Table(
    'tag_blog', db.Column('tags_id', db.Integer, db.ForeignKey('tags.id')),
    db.Column('blogs_id', db.Integer, db.ForeignKey('blogs.id')))


class Tags(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    blogs = db.relationship(
        'Blog', secondary=tag_blog, lazy='dynamic', backref="tags")

    def __repr__(self):
        return '<Tags %r>' % self.name


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.name

    def __str__(self):
        return self.name


class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())
    content = db.Column(db.Text, nullable=False)
    is_copy = db.Column(db.Boolean, nullable=True, default=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship(
        'Category', backref=db.backref(
            'blogs', lazy='dynamic'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship(
        'User', backref=db.backref(
            'blogs', lazy='dynamic'))

    __mapper_args__ = {"order_by": created_at.desc()}

    def __repr__(self):
        return "<Blog %r>" % self.title

    @classmethod
    def get(cls, blogId):
        return cls.query.filter_by(id=blogId).first_or_404()

    @classmethod
    def get_blog_list(cls, page=1, filter_dict=dict()):
        per_page = current_app.config['PER_PAGE']
        bloglist = cls.query
        if 'tag' in filter_dict.keys():
            tag = filter_dict.pop('tag')
            bloglist = bloglist.join(cls.tags).filter(Tags.name == tag)
        if 'category' in filter_dict.keys():
            category = filter_dict.pop('category')
            bloglist = bloglist.filter(cls.category == category)
        bloglist = bloglist.paginate(page, per_page, True)
        return bloglist


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow(), nullable=False)
    content = db.Column(db.Text, nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))
    blog = db.relationship(
        'Blog', backref=db.backref(
            'comments', lazy='dynamic'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship(
        'User', backref=db.backref(
            'comments', lazy='dynamic'))

    # def __init__(self, author, content):
    #     self.author = author
    #     self.content = content

    def __repr__(self):
        return "<Comment %r>" % self.content

    @classmethod
    def get_comment_list(cls, page=20, filter_dict=None):
        per_page = current_app.config['PER_PAGE']
        if filter_dict is None:
            return cls.query.paginate(page, per_page, True)
        commentlist = cls.query.filter_by(**filter_dict).paginate(
            page, per_page, True)
        return commentlist
