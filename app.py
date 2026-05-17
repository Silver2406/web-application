import requests
from flask import Flask, render_template, request, url_for, redirect
from flask_mysqldb import MySQL


app = Flask(__name__)
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '2807'
app.config['MYSQL_DB'] = 'deans_office'

mysql = MySQL(app)

AUTH_URL = "http://127.0.0.1:5002"



@app.route('/')
def home():
    return render_template('index.html')


@app.route("/login", methods=['POST'])
def login():
    username = request.form.get('логин')
    password = request.form.get('user_password')

    # Отправляем запрос к сервису авторизации
    resp = requests.post(f"{AUTH_URL}/login",
                         data={'логин': username, 'user_password': password})

    if resp.status_code == 200:
        token = resp.json().get('access_token')

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id_направления FROM training")
        trainings = cursor.fetchall()

        cursor.execute(
            'INSERT  users (логин, token, user_password) VALUES (%s, %s,%s)',
            (username, token, password)
        )
        mysql.connection.commit()
        cursor.close()

        response = redirect(url_for('login'))
        response.set_cookie('access_token', token, httponly=True)
        return render_template("index_1.html", trainings=trainings)
    else:
        return render_template('index.html', error="Неверный логин или пароль"), 401

@app.route("/password_reset", methods=['POST','GET'])
def password_reset():
    message=''
    if request.method == 'POST':
        email = request.form.get('email')
        user_password = request.form.get('user_password')
        new_password = request.form.get('new_password')
        cursor = mysql.connection.cursor()

        # Проверка, существует ли пользователь
        cursor.execute('SELECT * FROM registration WHERE email = %s AND user_password =%s',
                       (email,user_password))

        account = cursor.fetchone()

        if account:
            cursor.execute(
                'INSERT password_recovery  (new_password,email) VALUES(%s,%s)',
                (new_password,email)
            )
            mysql.connection.commit()
            message = 'Пароль успешно изменен!'
        else:
            message = 'Пользователь с таким email не найден!'

        cursor.close()
        return render_template('index.html', message=message)
    else:
        return render_template('password_recovery.html', message=message)

@app.route("/feedback", methods=['GET', 'POST'])
def feedback():
    return render_template('feedback.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration():

    if request.method == 'POST':
        user_name = request.form.get('user_name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        user_password = request.form.get('user_password')

        cursor = mysql.connection.cursor()

        # Проверка, существует ли пользователь
        cursor.execute('SELECT * FROM registration WHERE email = %s', (email,))
        account = cursor.fetchone()

        if not account:
            cursor.execute(
                'INSERT INTO registration (user_name, phone, email, user_password) VALUES (%s, %s, %s, %s)',
                (user_name, phone, email, user_password)
            )
            mysql.connection.commit()

        cursor.close()
        return render_template('index.html')
    else:
     return render_template('registration.html')




if __name__ == '__main__':
    app.run(port=5001,debug=True)