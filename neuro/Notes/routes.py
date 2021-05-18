from flask import render_template, url_for, flash, redirect,request,Blueprint
from neuro import app,db,bcrypt
from neuro.models import User, Day, Note
from neuro.Notes.forms import NoteForm
from flask_login import login_user, current_user, logout_user,login_required
from sqlalchemy import text

Notes = Blueprint('Notes',__name__)

####### Main Notes page #######
@Notes.route("/notes",methods=['GET','POST'])
@login_required
def notes():
    note = Note.query.filter_by(user_id=current_user.id)
    return render_template("notes.html",note=note)
    

@Notes.route("/notes/add",methods=['GET','POST'])
@login_required
def addNotes():
    form = NoteForm()
    if form.validate_on_submit():
        note = Note(title=form.title.data, text=form.text.data, user_id=current_user.id)
        db.session.add(note)
        db.session.commit()
        message = "Odpowiedz została wysłana!"
        return redirect(url_for('Notes.notes'))
    return render_template("add_notes.html",form=form)

@Notes.route("/notes/<int:note_id>",methods=['GET','POST'])
@login_required
def editNotes(note_id):
    note = Note.query.get_or_404(note_id)
    form = NoteForm()
    if form.validate_on_submit():
        note = Note.query.filter_by(id=note_id).update(dict(title=form.title.data, text=form.text.data))
        db.session.commit()
        return redirect(url_for('Notes.notes'))
    note_sql = db.engine.execute(text("SELECT title,text FROM note WHERE id = :id ").execution_options(autocommit=True),{'id': note_id})
    for notes in note_sql:
        print(notes[0])
    form.title.default = notes[0]
    form.text.default = notes[1]
    form.process()
    return render_template("edit_note.html",note=note, form=form,title=notes[0])

@Notes.route("/notes/<int:note_id>/delete", methods=['GET','POST'])
@login_required
def deleteNotes(note_id):
    note = Note.query.get_or_404(note_id)
    note1 = Note.query.filter_by(id=note_id).first()
    note2 = Note.query.filter_by(user_id=current_user.id)
    db.session.delete(note1)
    db.session.commit()
    return render_template("notes.html",note=note2)