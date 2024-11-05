import os
from flask import Flask, jsonify, abort, request, url_for, redirect
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import jwt
from dotenv import load_dotenv

# To load the ennvrionment variables from the .env file
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
app.config['extensions'] = ['.jpg','.pdf','.png']
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 #limiting the size of uploaded files
app.config['UPLOAD_PATH'] = 'uploads'

# MySQL configurations Testing
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'password')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'flask_app')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Checking to see if the folder exists
if not os.path.exists(app.config['UPLOAD_PATH']):
    os.makedirs(app.config['UPLOAD_PATH'])

# Public Route to get usernmane and ID
@app.route('/public', methods=['GET'])
def public_view():
    cursor = mysql.connection.cursor()
    query = "SELECT id, usernamen FROM users"
    cursor.execute(query)
    users = cursor.fetchall()
    cursor.close()
    return jsonify(users)

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

#login endpoint that aunthenticates user 
    if auth and 'username' not in auth or 'password' not in auth:
        return jsonify({'message': 'Invalid credentials!'}), 400
    
    # Using the username and password
    username = auth['username']
    password = auth['password']

    # Querying the database for the user
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM users WHERE usernmane = %s AND password = %s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    cursor.close()

    #Simple if conditons
    if user:
        token = jwt.encode({''})
        return jsonify({"message:" f'Welcome, {user['username']}!'})
    else:
        return jsonify({"message:" f'Invalid Credentials!'}), 401

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

# File Handling 

#upload file
@app.route('/upload')
def upload():
    return '''
        <html>
        <form action="/sendFile" method="POST" enctype="multipart/form-data">
            <input type="file" name="file"/><br>
            <input type="submit"/>
        </form>
        </html>
    '''

@app.route('/sendFile', methods=['POST', 'GET'])
def sendFile():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        filename = secure_filename(uploaded_file.filename)
        if os.path.splitext(filename)[1] in app.config['extensions']:
            uploaded_file.save(os.path.join(app.config['UPLOADS'],filename))
            return 'correct'
    return ''
if __name__ == '__main__':
    app.run(debug=True)