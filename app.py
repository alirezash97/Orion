from flask import Flask,render_template,request,url_for,session
from flask_sqlalchemy import SQLAlchemy
import os
from flask import make_response

from sqlalchemy import update
from sqlalchemy import exc
#session = []
login_flag = 0
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/orion.db'
db = SQLAlchemy(app)
app.debug = True

#migrate = Migrate(app, db)
class Person(db.Model):
    username = db.Column(db.String(80), primary_key=True)
    password = db.Column(db.String(120), unique=False, nullable=False)
    access_level = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return '<Person %r>' % self.username

class details(db.Model):

    username = db.Column(db.String(120),unique=True, nullable=False)
    fullname = db.Column(db.String(120), unique=False, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False,primary_key=True)
    password = db.Column(db.String(120), unique=False, nullable=True)
    gender = db.Column(db.String(120), unique=False, nullable=True)
    birthday = db.Column(db.String(120), unique=False, nullable=True)

    def __repr__(self):
            return '<signup %r>' % self.email


class create_event(db.Model):

    date = db.Column(db.String(120), unique=False, nullable=True)
    firstname = db.Column(db.String(120),unique=False, nullable=False)
    lastname = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False,primary_key=True)
    gender = db.Column(db.String(120), unique=False, nullable=True)
    birthday = db.Column(db.String(120), unique=False, nullable=True)
    subject =  db.Column(db.String(120), unique=False, nullable=False)
    abstract = db.Column(db.String(1000), unique=False, nullable=True)




    def __repr__(self):
            return '<event %r>' % self.email


@app.route('/authorization', methods=['GET', 'POST'])
def authorization():
    login_flag = 0
    username = request.form.get("Username")
    password = request.form.get("Password")
    exists = db.session.query(
        db.session.query(details).filter_by(username=username).exists()
    ).scalar()
    if exists and details.query.filter_by(username=username).first().password == password:
        access = Person.query.filter_by(username=username).first().access_level
        session[username] = (request.form.get('Username'),access)
        session['user'] = True
        if access == 'admin':
            session['admin'] = True
        render_template('home.html')
    else:
        return render_template('login.html')
    if request.method == "POST":
        if access == "admin":
#            session.append(2)
            login_flag = 2
            return render_template('home.html',login_flag = login_flag)
        elif access == "user":
#            session.append(1)
            login_flag = 1
            full_name = details.query.filter_by(username=username).first().fullname
            print(login_flag)
            return render_template('home.html',login_flag = login_flag,full_name = full_name)
        else:
            return render_template('login.html',login_flag=login_flag)
    else:
        return render_template('login.html',login_flag=login_flag)


@app.route('/signup_', methods=['GET', 'POST'])
def signup_():
    username_s = request.form.get("Username_s")
    fullname_s = request.form.get("Fullname_s")
    password_s = request.form.get("Password_s")
    email_s = request.form.get("Email_s")
    gender_s = request.form.get("gender_s")
    birthday_s = request.form.get("year_s")

    if request.method == "POST":
        db.create_all()
        new_person = Person(username=username_s,
                           password=password_s,
                           access_level='user')
        db.session.add(new_person)
        db.session.commit()
        new_user = details(username=username_s,
                          fullname=fullname_s,
                          email=email_s,
                          password=password_s,
                          birthday=birthday_s,
                          gender=gender_s)
        db.session.add(new_user)
        db.session.commit()
        return render_template('home.html')
    else:
        return render_template('login.html')


@app.route('/event_create', methods=['GET', 'POST'])
def event_create():
    date_c = request.form.get("date_c")
    firstname_c = request.form.get("firstname_c")
    lastname_c =  request.form.get("lastname_c")
    email_c =  request.form.get("email_c")
    gender_c = request.form.get("gender_c")
    birthday_c = request.form.get("year_c")
    subject_c = request.form.get("subject_c")
    abstract_c = request.form.get("abstract_c")
    if request.method == "POST":
        new_event = create_event(date = date_c,
                           firstname=firstname_c,
                           lastname=lastname_c,
                           email=email_c,
                           birthday=birthday_c,
                           gender=gender_c,
                           subject=subject_c,
                           abstract=abstract_c)
        db.session.add(new_event)
        db.session.commit()
        return render_template('home.html')



@app.route('/')
def home():
#    login_flag = 0
    return render_template('home.html',login_flag = login_flag)


@app.route('/event1.html')
def event1():
    return render_template('event1.html')


@app.route('/event2.html')
def event2():
#    if login_flag == 1:
        return render_template('home.html')


@app.route('/event3.html')
def event3():
#    if login_flag == 1:
        return render_template('home.html')



@app.route('/home.html')
def home_():
#    if session:
#        login_flag=0
#    else:
#        login_flag=1

    return render_template('home.html')


@app.route('/Events.html')
def Events():
#    if session:
#        login_flag=0
#    else:
#        login_flag=1
    return render_template('Events.html',create_event=create_event,login_flag=login_flag)


@app.route('/login.html')
def login():
    return render_template('login.html',login_flag=login_flag)


@app.route('/new_event.html')
def new_event():
    return render_template('new_event.html',login_flag=login_flag)


@app.route('/edit_event.html')
def edit_event():
    edit = request.form.get('edit_c')
    if request.method == "POST":
        print("haaaaaaaaaaaaaa")
        x = create_event.query.filter_by(email=edit).first()
        db.session.delete(x)
        db.session.commit()
        return render_template('home.html')
    else:
        return render_template('home.html')



@app.errorhandler(404)
def page_not_found(e):
    return render_template('Error404.html'), 404



@app.errorhandler(403)
def permission(error):
    return render_template('Error403.html'), 403


app.secret_key = os.urandom(20)

if __name__ == '__main__':
    app.run()

