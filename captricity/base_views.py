from flask import Blueprint, render_template

base_views = Blueprint('base_views', __name__, static_folder= "static", template_folder= "templates")


@base_views.route('/')
def index():
    return render_template('index.html')
