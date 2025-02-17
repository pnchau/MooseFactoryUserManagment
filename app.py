import os
import mysql.connector
from flask import Flask
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

DB_HOST = os.getenv("DB_HOST", "moosefactorydb.mysql.database.azure.com")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "moose")
DB_PASS = os.getenv("DB_PASS", "Moosefactory123")
DB_NAME = os.getenv("DB_NAME", "moosefactory_sql")

def get_db_connection():
    try:
        logging.info(f"Connecting to MySQL at {DB_HOST}:{DB_PORT} as {DB_USER}")
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
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

    cursor = conn.cursor(buffered=True)

    try:
        # Helper function to execute SQL scripts safely
        def execute_sql_file(filename):
            with open(filename, "r") as f:
                sql_script = f.read()
            for statement in sql_script.split(";"):
                if statement.strip():
                    cursor.execute(statement)
                    if statement.strip().lower().startswith("select"):
                        cursor.fetchall()  
                        
        execute_sql_file("database_template.sql")
        execute_sql_file("default_dataset.sql")
        execute_sql_file("test_case.sql")

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
