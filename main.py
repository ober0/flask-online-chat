import json
import random
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
import secrets

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

app.secret_key = secrets.token_hex(16)

app.config['MAIL_SERVER'] = 'smtp.yandex.ru'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_DEFAULT_SENDER'] = ''

mail = Mail(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    status = db.Column(db.Integer, default=0)



@app.route('/')
def index():
    if 'auth' in session:
        if session['auth']:
            return render_template('index.html', username=User.query.filter_by(id=session['account']).first().name)

    session['auth_data'] = ''
    session['auth_code'] = ''
    emails = [user.email for user in User.query.all()]
    return render_template('auth.html', emails=emails)


@app.route('/auth', methods=['POST'])
def auth():
    if request.method == "POST":
        for user in User.query.all():
            if str(user.email) == str(request.json.get('email')):
                if str(user.password) == str(request.json.get('password')):
                    session['auth'] = True
                    session['account'] = user.id
                    return jsonify({
                        'result': True
                    }), 200
        return jsonify({
            'result': False
        }), 401


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if request.method == "GET":
        return render_template('reg.html', emails = [user.email for user in User.query.all()])

    if request.method == "POST":

        name = request.json.get('name')
        email = request.json.get('email')
        password = request.json.get('password')


        session['auth_data'] = f'{name}:%:%:{email}:%:%:{password}'

        if email not in [i.email for i in User.query.all()]:
            return jsonify({
                'result': True
            }), 200


        return jsonify({
            'result': False

        }), 401


@app.route('/confirm_email', methods=['GET', 'POST'])
def confirm_email():
    if request.method == "GET":
        data = session.get('auth_data').split(':%:%:')
        email = data[1]
        code = random.randint(100000, 999999)
        msg = Message('Код подтверждения', recipients=[email])
        with open('templates/send.html', 'r', encoding='utf-8') as f:
            text = f.read()
            textSplit = text.split('//////')
            textSplit.append(textSplit[1])
            textSplit[1] = str(code)
            result = ''.join(textSplit)
        msg.html = result
        mail.send(msg)
        session['auth_code'] = code

        return render_template('confirm_email.html', email=email)
    else:
        code = request.json

        if str(code) == str(session['auth_code']):
            data = session.get('auth_data').split(':%:%:')
            user = User(name=data[0], email=data[1], password=data[2], status=0)
            try:
                db.session.add(user)
                db.session.commit()

                session['auth'] = True
                session['account'] = user.id
                session['auth_data'] = ''
                session['auth_code'] = ''

                return jsonify({
                    'res': True
                }), 200

            except Exception as e:
                print(e)
                db.session.rollback()

        return jsonify({
            'res': False
        }), 401


@app.route('/exit')
def exit():
    session['auth'] = False
    session['account'] = ''
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
