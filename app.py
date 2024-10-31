from flask import Flask, jsonify, abort, request
from flask_mysqldb import MySQL
import jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
#  @app.route('/')

# Error Handling

#error 400
@app.errorhandler(400)
def bad_request(e):

    return jsonify(error=str(e)), 400

#error 401
@app.errorhandler(401)
def unauthorized(e):

    return jsonify(error=str(e)), 401

#error 404
@app.errorhandler(404)
def page_not_found(e):

    return jsonify(error=str(e)), 404

#error 500
@app.errorhandler(500)
def internal_server_error(e):

    return jsonify(error=str(e)), 500

# Authentication

# login route to generate JWT token and create user model with username and password fields
@app.route('/login', methods=['POST'])
def login():
    auth = request.get_json()

#login endpoint that aunthenticates user and returns a jwt token 
    if auth and auth['username'] == 'admin' and auth['password'] == 'password':
        token = jwt.encode({'username': auth['username']}, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token})
    
    return jsonify({'message': 'Invalid Credentials!'}), 401

# protected endpoint that requires a valid jwt token to access
@app.route('/protected', methods=['GET'])
def protected():
    token = request. headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token is missing.'})
    
    # Strip "Bearer " prefix if it exists
    if token.startswith("Bearer "):
        token = token.split(" ")[1]

    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return jsonify({'message': f'Welcome, {data['username']}!'})
    except:
        return abort(404)
if __name__ == '__main__':
    app.run(debug=True)