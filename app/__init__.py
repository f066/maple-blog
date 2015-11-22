#*************************************************************************
#   Copyright © 2015 JiangLin. All rights reserved.
#   File Name: __init__.py
#   Author:JiangLin
#   Mail:xiyang0807@gmail.com
#   Created Time: 2015-11-18 08:03:11
#*************************************************************************
#!/usr/bin/env python
# -*- coding=UTF-8 -*-
from flask import Flask
from flask.ext.assets import Environment, Bundle
from flask_flatpages import FlatPages
from config import load_config


def create_app():
    app = Flask(__name__)
    config = load_config()
    app.config.from_object(config)

    register_routes(app)
    register_assets(app)
    register_db(app)
    register_jinja2(app)

    return app

def register_routes(app):
    from .views import admin, blog, book
    app.register_blueprint(admin.site, url_prefix='')
    app.register_blueprint(blog.site, url_prefix='/blog')
    app.register_blueprint(book.site, url_prefix='/book')

def register_db(app):
    from .models import db

    db.init_app(app)


def register_jinja2(app):
    app.jinja_env.add_extension('jinja2.ext.loopcontrols')

def register_assets(app):
    bundles = {

        'home_js': Bundle(
            'style/js/jquery.min.js',      #这里直接写static目录的子目录 ,如static/bootstrap是错误的
            'style/js/bootstrap.min.js',
            output='assets/home.js',
            filters='jsmin'),

        'home_css': Bundle(
            'style/css/bootstrap.min.css',
            output='assets/home.css',
            filters='cssmin')
        }

    assets = Environment(app)
    assets.register(bundles)

