from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    template = render_template('index.html')
    if (request.method == 'POST'):
        newNote = request.form['newNote']
        return newNote['title']
    return template

@app.route('/hello')
def hello_world():
    return 'Hello World!meowmwow'


if __name__ == '__main__':
    app.debug = True
    app.run()
