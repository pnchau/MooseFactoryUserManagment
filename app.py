import os
import mysql.connector
from flask import Flask
import logging

app = Flask(__name__)

# Load database config from Azure environment variables
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def get_db_connection():
    try:
        logging.info(f"Attempting to connect to MySQL at {DB_HOST} as {DB_USER}")
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            port=3306
        )
        logging.info("Database connection successful")
        return conn
    except mysql.connector.Error as err:
        logging.error(f"Database connection error: {err}")
        return None

@app.route("/init-db")
def init_db():
    conn = get_db_connection()
    if conn is None:
        return "Database connection failed", 500

    cursor = conn.cursor()

    try:
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
        cursor.close()
        conn.close()
        return "Database initialized successfully!"

    except mysql.connector.Error as err:
        logging.error(f"SQL execution error: {err}")
        return f"SQL Execution Error: {err}", 500

@app.route("/")
def home():
    return "Hello, this is my Flask app running on Azure!"

if __name__ == "__main__":
    app.run()
