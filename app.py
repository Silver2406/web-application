from authx import AuthX, AuthXConfig
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)



@app.route('/')
def home():
    return render_template('index.html')


@app.route("/greet", methods=['POST'])
def greet():
    username = request.form.get('username')
    password = request.form.get('password')
    if username == "test" and password == "test":
        return render_template('index_1.html')
    return None


@app.route("/password_reset", methods=['GET'])
def password_reset():
    return render_template('password_recovery.html')


@app.route("/feedback", methods=['GET', 'POST'])
def feedback():
    return render_template('feedback.html')


@app.route("/about")
def about():
    return


@app.route("/login", methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == "test" and password == "test":
        token = security.create_access_token(uid=username)
        response = redirect(url_for('protected'))
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return response
    else:
        return render_template('index.html', error="Неверный логин или пароль"), 401


@app.route('/protected', methods=['GET'])
def protected():
    security.access_token_required(lambda: None)
    return render_template ("index_1.html")


if __name__ == '__main__':
    app.run(debug=True)