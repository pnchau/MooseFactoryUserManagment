import os
import mysql.connector
from flask import Flask

app = Flask(__name__)

# Load database config from Azure environment variables
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

# Function to connect to the database
def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )

@app.route("/init-db")
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Run database_template.sql
    with open("database_template.sql", "r") as f:
        sql_script = f.read()
    for statement in sql_script.split(";"):
        if statement.strip():
            cursor.execute(statement)

    # Run default_dataset.sql
    with open("default_dataset.sql", "r") as f:
        sql_script = f.read()
    for statement in sql_script.split(";"):
        if statement.strip():
            cursor.execute(statement)

    # Run test_case.sql
    with open("test_case.sql", "r") as f:
        sql_script = f.read()
    for statement in sql_script.split(";"):
        if statement.strip():
            cursor.execute(statement)

    conn.commit()
    conn.close()
    return "Database initialized successfully!"
    
@app.route("/")
def home():
    return "Hello, this is my Flask app running on Azure!"

if __name__ == "__main__":
    app.run(debug=True)
