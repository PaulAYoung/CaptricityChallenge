#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from captricity.base_views import base_views
from captricity.images import image_views
from captricity.models import db_session
from captricity.auth import login_manager, auth_views

app = Flask(__name__)
login_manager.init_app(app)

@app.teardown_appcontext
def shutdown_session(exception=None):
    "Closes the db connections on shutdown"
    db_session.remove()

app.register_blueprint(base_views)
app.register_blueprint(image_views)
app.register_blueprint(auth_views)
