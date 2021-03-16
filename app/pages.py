from flask import Markup

import functools
import os
import boto3, botocore
from app.config import S3_KEY, S3_SECRET, S3_BUCKET, S3_LOCATION

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

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

def upload_file(file, bucket_name, acl="public-read"):
    print(S3_KEY, S3_SECRET)
    s3 = boto3.client("s3", aws_access_key_id=S3_KEY, aws_secret_access_key=S3_SECRET)
    try:
        s3.upload_fileobj(file, bucket_name, file.filename, ExtraArgs={"ACL": acl, "ContentType": file.content_type})
    except Exception as e:
        print("Unable to upload file:", e)
        return e
    return "{}{}".format(S3_LOCATION, file.filename)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['cpp', 'py', 'pdf']

@bp.route('/upload', methods=['POST'])
@login_required
def upload():
    if request.method == 'POST':
        if "file" not in request.files:
            return "No file uploaded"
        file = request.files['file']
        print(type(file))
        #sent file to S3
        if file.filename == "":
            return "Please select a file"
        if file and allowed_file(file.filename):
            print(file.filename)
            file.filename = secure_filename(file.filename)
            output = upload_file(file, S3_BUCKET)
            return str(output)
    return render_template('pages/submission.html')


@bp.route('/submission')
@login_required
def submission():
    return render_template('pages/submission.html')