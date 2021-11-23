from flask import Blueprint, render_template
from flask_login.utils import login_required

"""
    Note that in the below code, some arguments are specified when createing blueprint objects
    The first argument, 'site' is the Blueprint's name, which flask uses for routing
    The second arugment, __name__, is the blueprint's import name which flask uses to locate the Blueprint's resources
"""

site = Blueprint('site',__name__,template_folder = 'site_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile')
@login_required
def profile():
    return render_template('profile.html')