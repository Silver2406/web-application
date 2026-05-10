
from authx import AuthX, AuthXConfig
from flask import Flask, request,  jsonify

app = Flask(__name__)
authorization_url="http://127.0.0.1:5001"
config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)



@app.route("/login", methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == "test" and password == "test":
        token = security.create_access_token(uid=username)
        return jsonify({"access_token": token})
    return None


@app.route("/verify", methods=['POST'])
def verify():
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"valid": False}), 401

        token = auth_header.split(' ')[1]
        try:
            # Проверяем токен через AuthX
            security.access_token_required(lambda: None)
            return jsonify({"valid": True}), 200
        except Exception:
            return jsonify({"valid": False}), 401


if __name__ == '__main__':
    app.run(port= 5002, debug=True)