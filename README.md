# Building a RESTful API with Flask - Error Handling, Authentication, and File Handling with Public and Admin Routes

A RESTful API using Flask that covers
error handling, authentication, and file handling

## Team Members
- Ariel Monterrosas 
- Elizabeth Orellana

## Prerequisites
- Python 3.x
- MySQL server
- pip (Python package installer)

## How to Setup
1. **Clone the Repository**
   ```bash
   git clone https://github.com/zarakiliz/CPSC449-midterm-project
   cd CPSC449-midterm-project

2. **Create a Virtual Enviornment**
   ``` python3 -m venv venv
    source venv/bin/activate    
    On Windows, use `venv\Scripts\activate`

3. **Install Dependencies**
    ``` pip install -r requirements.txt

4.  **Environment Variables** 
    ```Create a .env file in the project root with the following entries: 
    SECRET_KEY=your_secret_key
    MYSQL_USER=your_mysql_user
    MYSQL_PASSWORD=your_mysql_password
    MYSQL_DB=your_mysql_db_name

5. **Set up MYSQL Database**
    ```Start your MySQL server and create a database.

    CREATE DATABASE CPSC449-midterm-project

    Update the .env file to match your MySQL credentials

6. **Run the Application**
   ``` flask run

