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
    return render_template('topic.html', topic = topic, notes = notes)

@app.route('/topic/<int:topic_id>/delete/', methods=['GET', 'POST'])
def deleteTopic(topic_id):
    topic = session.query(Topic).filter_by(id = topic_id).one()
    if (request.method == 'POST'):
        session.delete(topic)
        session.commit()
        return redirect(url_for('home'))
    return render_template('delete-topic.html', topic = topic)

@app.route('/hello')
def hello_world():
    return 'Hello World!meowmwow'


if __name__ == '__main__':
    app.debug = True
    app.run()
