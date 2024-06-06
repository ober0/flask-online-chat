import random
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, json
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
import secrets
from sqlalchemy import or_, and_


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


class Chats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    chat_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(1000), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    chat_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    new = db.Column(db.String(10), default='True')


@app.route('/clear', methods=['POST'])
def clear():
    if request.method == 'POST':
        self_id = session.get('account')
        chat_id = request.json.get('chat')

        for i in Message.query.all():
            print(i.user_id, i.chat_id, self_id,chat_id)
            if (int(i.user_id) == int(self_id) and int(i.chat_id) == int(chat_id)) or (int(i.user_id) == int(chat_id) and int(i.chat_id) == int(self_id)):
                db.session.delete(i)
                db.session.commit()

        return jsonify({'success': True})
    return ''

@app.route('/checkMsg', methods=['POST'])
def checkMsg():
    if request.method == "POST":
        id2 = request.json.get('from_id')
        id1 = session['account']



        messages = Message.query.filter(
            or_(
                and_(Message.chat_id == id2, Message.user_id == id1),
                and_(Message.chat_id == id1, Message.user_id == id2)
            )
        ).order_by(Message.id).all()

        for msg in messages:
            if msg.new == 'True':
                if msg.user_id != session['account']:
                    msg.new = 'False'
                    db.session.commit()
                    return jsonify({
                        'success': True,
                        'message': msg.message
                    })
        return jsonify({
            'success': False
        })

@app.route("/sendMsg", methods=['POST'])
def send_msg():
    if request.method == "POST":
        message_to = request.json.get('message_to')
        message = request.json.get('text_message')
        fromUseerId = session['account']

        message = Message(message=message, user_id=fromUseerId, chat_id=message_to)

        try:
            db.session.add(message)
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False})
    return jsonify({'success': False})
@app.route('/user/<int:user_id>', methods=['GET', 'POST'])
def user(user_id):

    if 'auth' in session and session['auth'] == True:

        if request.method == 'GET':
            user = User.query.filter_by(id=user_id).first()
            if user_id in [contact.chat_id for contact in Chats.query.filter_by(user_id=session['account']).all()]:
                added = True
            else:
                added = False
            return render_template('user.html', user=user, added=added)
        if request.method == 'POST':
            command = request.json['command']
            idToAdd = request.json['user_id']
            selfId = session['account']
            if command == 'add_user':
                if int(idToAdd) in [int(contact.chat_id) for contact in Chats.query.all()]:
                    return jsonify({
                        'result': False,
                        'message': 'Пользователь уже добавлен'
                    })
                chats = Chats(user_id=selfId, chat_id=idToAdd)
                try:
                    db.session.add(chats)
                    db.session.commit()
                    return jsonify({
                        'result': True,
                        'message': 'Успешно!'
                    })
                except Exception as e:
                    db.session.rollback()
                    return jsonify({
                        'result': False,
                        'message': str(e)
                    })

            elif command == 'remove_user':
                if int(idToAdd) in [int(contact.chat_id) for contact in Chats.query.all()]:
                    chatToRemove = Chats.query.filter_by(chat_id=idToAdd).filter_by(user_id=selfId).first()
                    try:
                        db.session.delete(chatToRemove)
                        db.session.commit()
                        return jsonify({
                            'result': True,
                            'message': 'Успешно!'
                        })
                    except:
                        db.session.rollback()
                        return jsonify({
                            'result': False,
                            'message': str(e)
                        })
                else:
                    return jsonify({
                        'result': False,
                        'message': 'Ошибка. Пользователь не в списке контактов!'
                    })
            else:
                return redirect('/')
    else:
        return redirect('/')
@app.route('/')
def index():
    if 'auth' in session and session['auth']:
        contacts_list = [i.chat_id for i in Chats.query.filter_by(user_id=session['account']).all()]
        contacts = []
        for i in contacts_list:
            contacts.append([i, User.query.filter_by(id=i).first().name])

        return render_template('index.html',
                               username=User.query.filter_by(id=session['account']).first().name,
                               contacts=contacts
                               )

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

@app.route("/chat/<int:chat_id>")
def chat(chat_id):
    if 'auth' in session and session['auth']:
        messages = Message.query.filter(
            or_(
                and_(Message.chat_id == chat_id, Message.user_id == session['account']),
                and_(Message.chat_id == session['account'], Message.user_id == chat_id)
            )
        ).order_by(Message.id).all()
        chat = Chats.query.filter_by(user_id=session['account']).filter_by(chat_id=chat_id).all()
        if len(chat) == 0:
            return redirect('/')
        return render_template('chat.html', user=User.query.filter_by(id=chat_id).first(), messages=messages)
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
