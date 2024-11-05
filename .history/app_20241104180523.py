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

# Root route
@app.route('/')
def home():
    return jsonify(message="Welcome to the Flask App! Try accessing /public, /login, or /protected endpoints.")


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
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # Serve the HTML login form
        return '''
            <html>
            <body>
                <h2>Login</h2>
                <form action="/login" method="POST">
                    <label for="username">Username:</label>
                    <input type="text" id="username" name="username" required><br><br>
                    
                    <label for="password">Password:</label>
                    <input type="password" id="password" name="password" required><br><br>
                    
                    <input type="submit" value="Login">
                </form>
            </body>
            </html>
        '''
    # elif request.method == 'POST':
    #     # Check if JSON data is provided
    #     if request.is_json:
    #         auth = request.get_json()
    #         username = auth.get('username')
    #         password = auth.get('password')
    #     else:
    #         # Handle form data from an HTML form
    #         username = request.form.get('username')
    #         password = request.form.get('password')

    #     # Validate that username and password are provided
    #     if not username or not password:
    #         return jsonify({'message': 'Invalid credentials!'}), 400

    # # Querying the database for the user
    # cursor = mysql.connection.cursor()
    # query = "SELECT * FROM users WHERE username = %s AND password = %s"
    # cursor.execute(query, (username, password))
    # user = cursor.fetchone()
    # cursor.close()

    #Simple if conditons
    # if user:
    #     token = jwt.encode({'usernamen': user['username']}, app.config['SECRET_KEY'], algorithm='HS256')
    #     # username = data['username']
    #     return jsonify({'message': f'Welcome, {username}! You have accessed the protected endpoint.'})
    # else:
    #     return jsonify({"message:" f'Invalid Credentials!'}), 401

# protected endpoint that requires a valid jwt token to access
@app.route('/protected', methods=['GET'])
def protected():
    token = request. headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token is missing.'}), 401
    
    # Strip "Bearer " prefix if it exists
    if token.startswith("Bearer "):
        token = token.split(" ")[1]

    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return jsonify({'message': f'Welcome, {data['username']}!'})
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401
if __name__ == '__main__':
    app.run(debug=True)
# File Handling 

# #upload file
# @app.route('/upload')
# def upload():
#     return '''
#         <html>
#         <form action="/sendFile" method="POST" enctype="multipart/form-data">
#             <input type="file" name="file"/><br>
#             <input type="submit"/>
#         </form>
#         </html>
#     '''

# @app.route('/sendFile', methods=['POST', 'GET'])
# def sendFile():
#     uploaded_file = request.files['file']
#     if uploaded_file.filename != '':
#         filename = secure_filename(uploaded_file.filename)
#         if os.path.splitext(filename)[1] in app.config['extensions']:
#             uploaded_file.save(os.path.join(app.config['UPLOADS'],filename))
#             return 'correct'
#     return ''
