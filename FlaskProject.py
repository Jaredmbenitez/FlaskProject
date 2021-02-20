# On windows: To start flask server WITH DEBUGGER
# 1) set FLASK_APP=FlaskProject.py
# 2) $env:FLASK_APP= "FlaskProject.py"
# 3) set FLASK_DEBUG=1
# 4)  $env:FLASK_DEBUG=1
# 5) flask run

from flask import Flask, render_template, url_for


app = Flask(__name__)


data = [
    {
        'author': 'Corey',
        'title': 'Blog Post 1',
        'content': 'First Post Content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Miky',
        'title': 'Blog Post 2',
        'content': 'Another Post Content',
        'date_posted': 'April 33, 2018'
    }
]


@app.route("/home")
@app.route("/")  # Root Page.
def home():
    return render_template('home.html', posts=data, title="Home")


@app.route("/about")  # About Page.
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
