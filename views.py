from flask.helpers import url_for
from werkzeug.utils import secure_filename
from .models import Run
from . import db
from flask import Blueprint, render_template, request, flash, redirect
from sqlalchemy.sql import func
from .static.logprocessor import *
import datetime

views = Blueprint('views', '__name__')

def convert_to_minutes(seconds):
    this_tuple = divmod(seconds,60)
    final_string = f"{this_tuple[0]} Minutes and {this_tuple[1]} Seconds"
    return final_string

@views.route('/')
def index():
    todays_run = Run.query.filter_by(date=func.current_date()).order_by(Run.time_taken.asc()).all()
    print(f"Today's runs: {todays_run}")
    return render_template("index.html", runs=todays_run, date=datetime.date.today() )

@views.route('/submit', methods=['GET','POST'])
def submit():
    if request.method == 'POST':
        username = request.form.get('username')
        if username == '':
            flash("Please enter a username", category="error")
        if 'file-upload' not in request.files:
            flash("No file uploaded", category="error")
            return redirect(request.url)
        file = request.files['file-upload']
        if file.filename == '':
            flash("No selected file", category="error")
            return redirect(request.url)
        elif file.filename != 'Client.txt':
            flash("Please submit the \"Client.txt\" file", category="error")
            return redirect(request.url)
        else:
            print("Post done") #Check if the file even made it past posting KEKW
            file.stream.seek(-1024*1024, 2) #Reads the last 1MB
            #Pass file to labladder module
            if not process_log(file.stream.read().decode('utf-8')):
                flash("No runs detected", category="error")
            else:
                time_taken = process_log(file.stream.read().decode('utf-8'))
                print("this is time taken {}".format(time_taken))    
                user_exist = Run.query.filter_by(username=username, date=func.current_date()).first()
                if user_exist:
                    user_exist.time_taken = time_taken
                    user_exist.minute_seconds = convert_to_minutes(time_taken)
                    db.session.commit()
                    flash("Record updated", category='sucess')
                    return redirect(url_for('views.index'))
                else:
                    new_run = Run(username=username, time_taken=time_taken, minute_seconds=convert_to_minutes(time_taken), date=func.current_date())
                    db.session.add(new_run)
                    db.session.commit()
                    return redirect(url_for('views.index'))


    return render_template("submit.html")