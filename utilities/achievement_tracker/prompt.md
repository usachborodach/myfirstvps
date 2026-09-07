Есть такой проект:

### tree -a /home/user/repos/myfirstvps/utilities/timetracker/:
```
/home/user/repos/myfirstvps/utilities/timetracker/
├── app.py
├── clean_duplicates.py
├── create_index.py
├── .env
├── prompt.md
├── requirements.txt
├── static
│   └── favicon.png
├── templates
│   ├── index.html
│   └── login.html
└── timetracker.service

2 directories, 10 files
```

### /home/user/repos/myfirstvps/utilities/timetracker/create_index.py:
```
from pymongo import MongoClient, ASCENDING
client = MongoClient('mongodb://localhost:27017/tracker')
db = client.get_database()
db.days.create_index([("date", ASCENDING)], unique=True)
```

### /home/user/repos/myfirstvps/utilities/timetracker/prompt.md:
```
Напиши python flask сервис чтобы я отслеживал сколько времени в день я трачу на разные вещи.
У меня есть vps сервер с mongodb.
Сервис должен быть с авторизацией. 
Нужно чтобы я мог пользоваться им и с телефона и с компьютера.
Оформление в стиле "тёмная тема". Тёмно-серые цвета

Каждый день ночью пусть создаётся документ:
```
{
    "date": (сегодняшний день в формате datetime),
    "hours": {
        "07:00": "",
        "09:00": "",
        "10:00": "",
        "11:00": "",
        "12:00": "",
        "13:00": "",
        "14:00": "",
        "15:00": "",
        "16:00": "",
        "17:00": "",
        "18:00": "",
        "19:00": "",
        "20:00": "",
        "21:00": ""
        "22:00": "",
        "23:00": ""
    }
}
```
Веб страничка будет выглядеть как табличка с этими данными, и можно будет выбирать для каждого часа активность из выпадающего списка.
Варианты:
- Работал
- Кодил для себя
- Время с семьёй
- Домашние задачи
- Залипал
- Спал

```

### /home/user/repos/myfirstvps/utilities/timetracker/clean_duplicates.py:
```
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

client = MongoClient(os.getenv('MONGO_URI', 'mongodb://localhost:27017/tracker'))
db = client.get_database()
collection = db.days

# Находим все даты, у которых больше одного документа
pipeline = [
    {"$group": {"_id": "$date", "count": {"$sum": 1}, "ids": {"$push": "$_id"}}},
    {"$match": {"count": {"$gt": 1}}}
]
duplicates = collection.aggregate(pipeline)

for dup in duplicates:
    date = dup['_id']
    ids = dup['ids']
    # Оставляем первый документ (самый старый по _id), остальные удаляем
    keep_id = ids[0]
    delete_ids = ids[1:]
    result = collection.delete_many({"_id": {"$in": delete_ids}})
    print(f"Дата {date}: удалено {result.deleted_count} дубликатов, оставлен {keep_id}")

print("Готово.")
```

### /home/user/repos/myfirstvps/utilities/timetracker/.env:
```
SECRET_KEY=***
MONGO_URI=mongodb://localhost:27017/tracker
USERNAME=admin
PASSWORD_HASH=***
```

### /home/user/repos/myfirstvps/utilities/timetracker/requirements.txt:
```
Flask==2.3.2
pymongo==4.5.0
Flask-Login==0.6.2
APScheduler==3.10.4
python-dotenv==1.0.0
Werkzeug==2.3.6
```

### /home/user/repos/myfirstvps/utilities/timetracker/templates/login.html:
```
<!DOCTYPE html>
<html lang="ru" data-bs-theme="dark">
<head>
    <link rel="icon" type="image/x-icon" href="{{ url_for('static', filename='favicon.png') }}">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>timetracker login</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #1e1e1e;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .card {
            background-color: #2d2d2d;
            border: 1px solid #3a3a3a;
            border-radius: 12px;
            padding: 1.5rem;
        }
        .form-control {
            background-color: #3a3a3a;
            border: 1px solid #4a4a4a;
            color: #e0e0e0;
        }
        .form-control:focus {
            background-color: #3a3a3a;
            border-color: #6c757d;
            color: #fff;
        }
        .btn-primary {
            background-color: #0d6efd;
            border-color: #0d6efd;
        }
        .btn-primary:hover {
            background-color: #0b5ed7;
        }
        .alert {
            background-color: #3a3a3a;
            border-color: #4a4a4a;
            color: #f8f9fa;
        }
        .card-header {
            border-bottom: 1px solid #3a3a3a;
            background-color: transparent;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-4">
                <div class="card">
                    <div class="card-header text-center">
                        <h4 class="text-light">timetracker</h4>
                    </div>
                    <div class="card-body">
                        {% with messages = get_flashed_messages(with_categories=true) %}
                            {% for category, message in messages %}
                                <div class="alert alert-{{ category }}">{{ message }}</div>
                            {% endfor %}
                        {% endwith %}
                        <form method="post">
                            <div class="mb-3">
                                <label for="username" class="form-label text-light">Логин</label>
                                <input type="text" class="form-control" id="username" name="username" required>
                            </div>
                            <div class="mb-3">
                                <label for="password" class="form-label text-light">Пароль</label>
                                <input type="password" class="form-control" id="password" name="password" required>
                            </div>
                            <button type="submit" class="btn btn-primary w-100">Войти</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
```

### /home/user/repos/myfirstvps/utilities/timetracker/templates/index.html:
```
<!DOCTYPE html>
<html lang="ru" data-bs-theme="dark">
<head>
    <link rel="icon" type="image/x-icon" href="{{ url_for('static', filename='favicon.png') }}">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>timetracker</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #1a1a1a;
            color: #e0e0e0;
        }
        .navbar {
            background-color: #2d2d2d !important;
            border-bottom: 1px solid #3a3a3a;
        }
        .navbar-brand, .navbar-text {
            color: #e0e0e0 !important;
        }
        .btn-outline-light {
            border-color: #4a4a4a;
            color: #e0e0e0;
        }
        .btn-outline-light:hover {
            background-color: #3a3a3a;
        }
        .btn-outline-secondary {
            border-color: #4a4a4a;
            color: #b0b0b0;
        }
        .btn-outline-secondary:hover {
            background-color: #3a3a3a;
            color: #fff;
        }
        .btn-outline-primary {
            border-color: #0d6efd;
            color: #0d6efd;
        }
        .btn-outline-primary:hover {
            background-color: #0d6efd;
            color: #fff;
        }
        .table {
            background-color: #2d2d2d;
            border-color: #3a3a3a;
            color: #e0e0e0;
        }
        .table th {
            background-color: #3a3a3a;
            border-color: #4a4a4a;
            color: #d0d0d0;
        }
        .table td {
            border-color: #3a3a3a;
            vertical-align: middle;
        }
        .table tbody tr:hover {
            background-color: #3d3d3d;
        }
        .activity-select {
            background-color: #3a3a3a;
            color: #e0e0e0;
            border: 1px solid #4a4a4a;
            border-radius: 4px;
            padding: 0.25rem 0.5rem;
            width: 100%;
        }
        .activity-select:focus {
            background-color: #4a4a4a;
            border-color: #6c757d;
        }
        .activity-select option {
            background-color: #2d2d2d;
            color: #e0e0e0;
        }
        .text-muted {
            color: #888888 !important;
        }
        .btn-group .btn {
            background-color: #2d2d2d;
            border-color: #3a3a3a;
            color: #d0d0d0;
        }
        .btn-group .btn:hover {
            background-color: #3a3a3a;
        }
        .btn-group .btn-outline-primary {
            background-color: #0d6efd;
            color: #fff;
            border-color: #0d6efd;
        }
        .btn-group .btn-outline-primary:hover {
            background-color: #0b5ed7;
        }
        @media (max-width: 576px) {
            .activity-select {
                font-size: 0.8rem;
                padding: 0.15rem 0.3rem;
            }
            .table th, .table td {
                padding: 0.3rem;
            }
            .btn-group .btn {
                font-size: 0.8rem;
                padding: 0.25rem 0.5rem;
            }
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg">
        <div class="container-fluid">
            <span class="navbar-brand">timetracker</span>
            <div class="d-flex">
                <span class="navbar-text me-3">{{ date.strftime('%d.%m.%Y') }}</span>
                <a href="{{ url_for('logout') }}" class="btn btn-outline-light btn-sm">Выйти</a>
            </div>
        </div>
    </nav>

    <div class="container mt-3">
        <!-- Навигация по датам -->
        <div class="row mb-3">
            <div class="col-12">
                <div class="btn-group w-100" role="group">
                    <a href="{{ url_for('index', date=date - timedelta(days=1)) }}" class="btn btn-outline-secondary">&laquo; Предыдущий</a>
                    <a href="{{ url_for('index') }}" class="btn btn-outline-primary">Сегодня</a>
                    <a href="{{ url_for('index', date=date + timedelta(days=1)) }}" class="btn btn-outline-secondary">Следующий &raquo;</a>
                </div>
            </div>
        </div>

        <!-- Таблица -->
        <div class="table-responsive">
            <table class="table table-bordered table-hover align-middle">
                <thead>
                    <tr>
                        <th style="width: 80px;">Время</th>
                        <th>Активность</th>
                    </tr>
                </thead>
                <tbody>
                    {% for hour in hours_list %}
                    <tr>
                        <td class="text-center fw-bold">{{ hour }}</td>
                        <td>
                            <select class="activity-select form-select form-select-sm" data-hour="{{ hour }}">
                                <option value="">—</option>
                                {% for activity in activities %}
                                    <option value="{{ activity }}" {% if hours[hour] == activity %}selected{% endif %}>
                                        {{ activity }}
                                    </option>
                                {% endfor %}
                            </select>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>

        <div class="text-muted small mt-2">
            <i>Изменения сохраняются автоматически при выборе активности.</i>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const selects = document.querySelectorAll('.activity-select');
            const currentDate = '{{ date.strftime("%Y-%m-%d") }}';

            selects.forEach(select => {
                select.addEventListener('change', function() {
                    const hour = this.dataset.hour;
                    const activity = this.value;

                    fetch('/update', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            date: currentDate,
                            hour: hour,
                            activity: activity
                        })
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (!data.success) {
                            alert('Ошибка сохранения: ' + (data.message || 'неизвестная ошибка'));
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        alert('Ошибка сети при сохранении');
                    });
                });
            });
        });
    </script>
</body>
</html>
```

### /home/user/repos/myfirstvps/utilities/timetracker/timetracker.service:
```
[Unit]
Description=Time Tracker Flask Service
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/root/myfirstvps/utilities/timetracker
EnvironmentFile=/root/myfirstvps/utilities/timetracker/.env
ExecStart=/usr/local/bin/gunicorn -w 4 -b 0.0.0.0:8001 app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### /home/user/repos/myfirstvps/utilities/timetracker/app.py:
```
import os
from datetime import datetime, time, timedelta
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from pymongo import MongoClient
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from werkzeug.security import generate_password_hash, check_password_hash


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-change-in-production')

# MongoDB
client = MongoClient(os.getenv('MONGO_URI', 'mongodb://localhost:27017/tracker'))
db = client.get_database()
days_collection = db.days

# Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Простая модель пользователя (один пользователь)
class User(UserMixin):
    def __init__(self, username):
        self.id = username

# Загрузка пользователя (по id)
@login_manager.user_loader
def load_user(user_id):
    if user_id == os.getenv('USERNAME'):
        return User(user_id)
    return None

# Проверка пароля (простая, в реальном проекте используйте хеши)
PASSWORD_HASH = os.getenv('PASSWORD_HASH')
def verify_password(username, password):
    return (username == os.getenv('USERNAME') and
            check_password_hash(PASSWORD_HASH, password))

# Список доступных активностей
ACTIVITIES = [
    'Обзор задач',
    'Работал',
    'Кодил для себя',
    'Домашние задачи',
    'Залипал',
    'Спал',
    'Время с семьёй',
    'Время с Юлочкой',
    'Время с Ваней',
    'Время с Таней',    
]

# Часы, которые будут отображаться
HOURS = [
    '07:00', '08:00', '09:00', '10:00', '11:00', '12:00',
    '13:00', '14:00', '15:00', '16:00', '17:00',
    '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'
]

# Функция создания документа дня
def create_day_record(date):
    hours_dict = {hour: '' for hour in HOURS}
    doc = {
        'date': datetime(date.year, date.month, date.day),
        'hours': hours_dict
    }
    days_collection.insert_one(doc)
    return doc

# Получить или создать запись за указанную дату
def get_or_create_day(date):
    # Преобразуем date в datetime (как хранится в БД)
    date_obj = datetime(date.year, date.month, date.day)
    
    # Пытаемся обновить или вставить документ атомарно
    result = days_collection.update_one(
        {'date': date_obj},
        {'$setOnInsert': {'hours': {hour: '' for hour in HOURS}}},
        upsert=True
    )
    # Возвращаем документ
    doc = days_collection.find_one({'date': date_obj})
    return doc

# Ежедневное создание записи на следующий день (запускается в 00:00)
def create_tomorrow_record():
    tomorrow = datetime.now().date() + timedelta(days=1)
    get_or_create_day(tomorrow)

# Инициализация планировщика
scheduler = BackgroundScheduler()
scheduler.add_job(
    func=create_tomorrow_record,
    trigger=CronTrigger(hour=0, minute=0),
    id='create_daily_record',
    replace_existing=True
)
scheduler.start()

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
    # Получаем дату из параметра или сегодня
    date_str = request.args.get('date')
    if date_str:
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            date_obj = datetime.now().date()
    else:
        date_obj = datetime.now().date()

    doc = get_or_create_day(date_obj)
    hours = doc['hours']
    return render_template('index.html',
                           date=date_obj,
                           hours=hours,
                           activities=ACTIVITIES,
                           hours_list=HOURS,
                           timedelta=timedelta)

@app.route('/update', methods=['POST'])
@login_required
def update():
    data = request.json
    date_str = data.get('date')
    hour = data.get('hour')
    activity = data.get('activity')

    if not date_str or not hour:
        return jsonify({'success': False, 'message': 'Недостаточно данных'}), 400

    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'success': False, 'message': 'Неверный формат даты'}), 400

    if hour not in HOURS:
        return jsonify({'success': False, 'message': 'Неверный час'}), 400

    if activity and activity not in ACTIVITIES:
        return jsonify({'success': False, 'message': 'Неверная активность'}), 400

    # Обновление в БД
    result = days_collection.update_one(
        {'date': datetime(date_obj.year, date_obj.month, date_obj.day)},
        {'$set': {f'hours.{hour}': activity}}
    )
    if result.matched_count:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Запись не найдена'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=False)
```

я хочу написать очень похожий проект, с таким же оформлением и технологиями. но с небольшим отличием:
- название achievment_tracker
- в нём я буду писать коротко о достижениях за день в трёх катгориях: personal_coding, work, home_tasks
- соответственно на странице будет три столбца и текстовые поля для заполнения