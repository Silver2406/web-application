from MySQLdb.cursors import DictCursor
from authx import AuthX, AuthXConfig
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL



app = Flask(__name__)
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '2807'
app.config['MYSQL_DB'] = 'deans_office'

mysql = MySQL(app)

config = AuthXConfig()
config.JWT_SECRET_KEY = "your-very-long-secret-key-minimum-32-characters!!!!"
config.JWT_ACCESS_COOKIE_NAME = "access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]





security = AuthX(config=config)
AUTH_URL = "http://127.0.0.1:5001"


@app.route("/login", methods=['POST'])
def login():
    # Получаем данные из формы (как в password_reset)
    login = request.form.get('логин')  # login пользователя
    user_password = request.form.get('user_password')  # пароль пользователя

    cursor = mysql.connection.cursor(DictCursor)

    # Проверка, существует ли пользователь (как в password_reset)
    cursor.execute('SELECT * FROM registration WHERE user_name = %s', (login,))
    account = cursor.fetchone()
    cursor.close()
    if account:
        # Пользователь существует → проверяем пароль
        if account['user_password'] == user_password:
            # Пароль верный → создаем токен
            token = security.create_access_token(uid=login)
            return jsonify({"access_token": token}), 200
        else:
            # Пароль неверный
            return jsonify({"error": "Неверный логин или пароль"}), 401
    else:
        # Пользователь не найден
        return jsonify({"error": "Пользователь с таким email не найден"}), 401




if __name__ == '__main__':
    app.run(port=5002, debug=True)