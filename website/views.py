from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import ToDo
from . import db
import json
from datetime import datetime


views = Blueprint('views', __name__)

@views.route('/', methods=["GET", "POST"])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('ToDo')


        if len(note) < 1:
            flash('To-Do is too short', category='error')
        if len(request.form['do_by']) < 1:
            flash('Date is invalid', category='error')
        else:
            do_by = datetime.strptime(
                     request.form['do_by'],
                     '%Y-%m-%dT%H:%M')
                    
            new_note = ToDo(data=note, do_by=do_by, isDone = False, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()

            print(new_note.data)


            flash('Note added', category='success')


    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = ToDo.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    
    return jsonify({})

@views.route('/mark-done', methods=['GET', 'POST'])
def mark_done():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = ToDo.query.get(noteId)
    print("No way")
    if note:
        if note.user_id == current_user.id:
            note.isDone = not note.isDone
            db.session.commit()
    
    return jsonify({})
