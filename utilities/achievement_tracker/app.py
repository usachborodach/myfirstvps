import os
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from pymongo import MongoClient
from dotenv import load_dotenv
from werkzeug.security import check_password_hash

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-change-in-production')

# MongoDB
client = MongoClient(os.getenv('MONGO_URI', 'mongodb://localhost:27017/achievements'))
db = client.get_database()
days_collection = db.days

# Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(user_id):
    if user_id == os.getenv('USERNAME'):
        return User(user_id)
    return None

PASSWORD_HASH = os.getenv('PASSWORD_HASH')
def verify_password(username, password):
    return (username == os.getenv('USERNAME') and
            check_password_hash(PASSWORD_HASH, password))

# Категории (они же заголовки колонок)
CATEGORIES = {
    'personal_coding': 'Кодил для себя',
    'work': 'Работал',
    'home_tasks': 'Домашние задачи'
}

# Получение или создание документа дня
def get_or_create_day(date_obj):
    # date_obj – объект date
    date_datetime = datetime(date_obj.year, date_obj.month, date_obj.day)
    doc = days_collection.find_one({'date': date_datetime})
    if doc is None:
        # Создаём пустую запись
        new_doc = {
            'date': date_datetime,
            'personal_coding': '',
            'work': '',
            'home_tasks': ''
        }
        days_collection.insert_one(new_doc)
        doc = new_doc
    return doc

# Роуты
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if verify_password(username, password):
            user = User(username)
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Неверный логин или пароль', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    date_str = request.args.get('date')
    if date_str:
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            date_obj = datetime.now().date()
    else:
        date_obj = datetime.now().date()

    doc = get_or_create_day(date_obj)
    # Передаём данные в шаблон
    return render_template('index.html',
                           date=date_obj,
                           doc=doc,
                           categories=CATEGORIES,
                           timedelta=timedelta)

@app.route('/update', methods=['POST'])
@login_required
def update():
    data = request.json
    date_str = data.get('date')
    category = data.get('category')
    text = data.get('text', '').strip()

    if not date_str or not category:
        return jsonify({'success': False, 'message': 'Недостаточно данных'}), 400

    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'success': False, 'message': 'Неверный формат даты'}), 400

    if category not in CATEGORIES:
        return jsonify({'success': False, 'message': 'Неверная категория'}), 400

    # Обновляем только указанное поле
    result = days_collection.update_one(
        {'date': datetime(date_obj.year, date_obj.month, date_obj.day)},
        {'$set': {category: text}}
    )
    if result.matched_count:
        return jsonify({'success': True})
    else:
        # Если документа нет, создаём (на случай гонки)
        get_or_create_day(date_obj)
        days_collection.update_one(
            {'date': datetime(date_obj.year, date_obj.month, date_obj.day)},
            {'$set': {category: text}}
        )
        return jsonify({'success': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8004, debug=False)  # порт можно изменить