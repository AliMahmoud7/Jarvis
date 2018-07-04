from flask import render_template, request, url_for,\
    redirect, jsonify, flash, Blueprint, send_from_directory
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, FileField, SubmitField, validators
from flask_wtf.file import FileField, FileAllowed, FileRequired
from werkzeug.utils import secure_filename
import os
from app import app, db
from flask_uploads import TEXT, DOCUMENTS, IMAGES, DATA, DEFAULTS, AUDIO, ARCHIVES
from app.models import *
import random
import string
import subprocess

data = Blueprint('data', __name__)


class NewForm(FlaskForm):
    message = TextAreaField('Message', [validators.length(max=255)])
    numbers = FileField('Numbers as Excel Sheet', [FileAllowed(['xls', 'xlsx'], 'Excel sheet only!')])
    file = FileField('Media or Other Files', [FileAllowed(DEFAULTS + AUDIO + ARCHIVES + ('pdf', 'ppt', 'pptx'))])


@data.route('/users/<int:user_id>/generate')
@login_required
@check_current_user
def generate_code(user_id):
    user = User.query.filter_by(id=user_id).one()
    code = user.generate_code()
    # user.revoke_code()
    db.session.add(user)
    db.session.commit()
    flash('Done! Your code is: {}'.format(code))
    return redirect(url_for('.show_data', user_id=user_id))


@data.route('/users/<int:user_id>/')
@login_required
@check_current_user
def show_data(user_id):
    if login_session.get('send'):
        try:
            login_session['browser'] = None
            login_session['numbers_path'] = None
            web_driver_quit()
            # subprocess.run('killall chromedriver', shell=True)
        except:
            pass
    numbers = Number.query.filter_by(user_id=user_id).all()
    files = File.query.filter_by(user_id=user_id).all()
    messages = Message.query.filter_by(user_id=user_id).all()
    return render_template('show_data.html', user_id=user_id, numbers=numbers, files=files, messages=messages)


@data.route('/users/<int:user_id>/new', methods=['GET', 'POST'])
@login_required
@check_current_user
def new_data(user_id):
    form = NewForm()
    if form.validate_on_submit():
        text = form.message.data
        if text:
            message = Message(text=text, user_id=user_id)
            db.session.add(message)
            db.session.commit()

        numbers = form.numbers.data
        if numbers:
            filename = secure_filename(numbers.filename)
            name, f_type = filename.rsplit('.', 1)[0], filename.rsplit('.', 1)[1].lower()
            num = len(Number.query.filter(Number.filename.like('{}%'.format(name))).all())
            if num:
                path = os.path.join(app.config['UPLOAD_FOLDER'], 'numbers', name + '({}).'.format(num) + f_type)
            else:
                path = os.path.join(app.config['UPLOAD_FOLDER'], 'numbers', filename)
            numbers.save(path)
            numbers_sheet = Number(filename=filename, f_type=f_type, path=path, user_id=user_id)
            if num:
                numbers_sheet.rename(num)
            db.session.add(numbers_sheet)
            db.session.commit()
            print('numbers saved!')

        file = form.file.data
        if file:
            for f in request.files.getlist('file'):
                filename = secure_filename(f.filename)
                name, f_type = filename.rsplit('.', 1)[0], filename.rsplit('.', 1)[1].lower()
                num = len(File.query.filter(File.filename.like('{}%'.format(name))).all())
                if num:
                    path = os.path.join(app.config['UPLOAD_FOLDER'], 'files', name + '({}).'.format(num) + f_type)
                else:
                    path = os.path.join(app.config['UPLOAD_FOLDER'], 'files', filename)
                f.save(path)
                new_file = File(filename=filename, f_type=f_type, path=path, user_id=user_id)
                if num:
                    new_file.rename(num)
                db.session.add(new_file)
                db.session.commit()
            print('files upload completed!')
        flash('Successfully added new data')

        return redirect(url_for('data.show_data', user_id=user_id))
    return render_template('new_data.html', form=form)


@data.route('/uploads/<folder_name>/<filename>')
def uploaded_file(folder_name, filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], folder_name), filename)


@data.route('/users/sheets/<int:user_id>/<int:sheet_id>/delete', methods=['GET', 'POST'])
@login_required
@check_current_user
def delete_sheet(user_id, sheet_id):
    numers_sheet = Number.query.filter_by(id=sheet_id).one()

    if request.method == 'POST':
        db.session.delete(numers_sheet)
        db.session.commit()
        flash('Sheet {} Successfully Deleted'.format(numers_sheet.filename))
        return redirect(url_for('data.show_data', user_id=user_id))

    return render_template('delete_sheet.html', numers_sheet=numers_sheet, user_id=user_id)


@data.route('/users/messages/<int:user_id>/<int:message_id>/delete', methods=['GET', 'POST'])
@login_required
@check_current_user
def delete_message(user_id, message_id):
    message = Message.query.filter_by(id=message_id).one()

    if request.method == 'POST':
        db.session.delete(message)
        db.session.commit()
        flash('Message Successfully Deleted')
        return redirect(url_for('data.show_data', user_id=user_id))

    return render_template('delete_message.html', message=message, user_id=user_id)


@data.route('/users/files/<int:user_id>/<int:file_id>/delete', methods=['GET', 'POST'])
@login_required
@check_current_user
def delete_file(user_id, file_id):
    file = File.query.filter_by(id=file_id).one()

    if request.method == 'POST':
        db.session.delete(file)
        db.session.commit()
        flash('File {} Successfully Deleted'.format(file.filename))
        return redirect(url_for('data.show_data', user_id=user_id))

    return render_template('delete_file.html', file=file, user_id=user_id)

