from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_setup import Base, Topic, Note

app = Flask(__name__)

engine = create_engine('sqlite:///noted.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/', methods=['GET', 'POST'])
def home():
    topics = session.query(Topic)
    if (request.method == 'POST'):
        newTopic = Topic(topic = request.form['newTopic'])
        session.add(newTopic)
        session.commit()
    return render_template('home.html', topics = topics)

@app.route('/topic/<int:topic_id>/', methods=['GET', 'POST'])
def topic(topic_id):
    topic = session.query(Topic).filter_by(id = topic_id).one()
    notes = session.query(Note).filter_by(topic_id = topic_id)
    if (request.method == 'POST'):
        newNote = Note(title = request.form['title'], message = request.form['message'], topic_id = topic_id)
        session.add(newNote)
        session.commit()
    return render_template('topic-page.html', topic=topic, notes=notes)

@app.route('/topic/<int:topic_id>/delete/', methods=['GET', 'POST'])
def deleteTopic(topic_id):
    topic = session.query(Topic).filter_by(id = topic_id).one()
    if (request.method == 'POST'):
        session.delete(topic)
        session.commit()
        return redirect(url_for('home'))
    return render_template('delete-topic.html', topic = topic)


@app.route('/topic/<int:topic_id>/rename/', methods=['GET', 'POST'])
def renameTopic(topic_id):
    topic = session.query(Topic).filter_by(id=topic_id).one()
    if (request.method == 'POST'):
        topic.topic = request.form['newTopic']
        session.commit()
        return redirect(url_for('home'))
    return render_template('rename-topic.html', topic=topic)


@app.route('/topic/<int:topic_id>/note/<int:note_id>/delete/', methods=['GET', 'POST'])
def deleteNote(topic_id, note_id):
    topic = session.query(Topic).filter_by(id=topic_id).one()
    note = session.query(Note).filter_by(topic_id=topic_id, id=note_id).one()
    if (request.method == 'POST'):
        session.delete(note)
        session.commit()
        return redirect(url_for('topic', topic_id=topic.id))
    return render_template('delete-note.html', topic=topic, note=note)


@app.route('/topic/<int:topic_id>/note/<int:note_id>/edit/', methods=['GET', 'POST'])
def editNote(topic_id, note_id):
    topic = session.query(Topic).filter_by(id=topic_id).one()
    note = session.query(Note).filter_by(topic_id=topic_id, id=note_id).one()
    if (request.method == 'POST'):
        note.title = request.form['title']
        note.message = request.form['message']
        session.commit()
        return redirect(url_for('topic', topic_id=topic.id))
    return render_template('edit-note.html', topic=topic, note=note)

@app.route('/hello')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.debug = True
    app.run()
