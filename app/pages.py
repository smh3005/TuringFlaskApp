from flask import Markup

import functools
import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db
from app.auth import login_required
import markdown

bp = Blueprint('pages', __name__)
print(os.getcwd())
with open('app/static/TestProblem.md', 'r') as f:
    text = f.read()
    html = Markup(markdown.markdown(text))

@bp.route('/')
def index():
    return render_template('pages/index.html', markdown=html)

@bp.route('/leaderboard')
@login_required
def leaderboard():
    return render_template('pages/leaderboard.html')

@bp.route('/account')
@login_required
def account():
    return render_template('pages/account.html')