# import os
# from sqlalchemy import create_engine, text
# from sqlalchemy.orm import Session
# from sqlalchemy.ext.automap import automap_base
# from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask import Flask, request, render_template, g
# from dotenv import load_dotenv
import mysql.connector
from mysql.connector import errorcode
import sys


app = Flask(__name__)
bootstrap = Bootstrap(app)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'N!n@T@z',
    'database': 'sakila',
    'auth_plugin':'mysql_native_password',
}

def get_db_connection():
    connection = mysql.connector.connect(host = 'localhost', user = 'root', password = 'N!n@T@z', database = 'sakila', auth_plugin = 'auth_plugin')
    return connection


@app.route('/')
def index():
    contributors = {
        'Brennan': 'Developer',
        'Micheal': 'Developer',
        'Nathan': 'Developer',
        'Daniela': 'Developer',
        # Add more contributors and roles here
    }
    tasks = {
        'Task 1': 'Brennan',
        'Task 2': 'Micheal',
        'Task 3': 'Daniela',
        'Task 4': 'Nathan'
        # Add more tasks and assignees here
    }
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="bhc2020!",
            database="sakila"
        )

        if mydb.is_connected():
            print("Connected to MySQL database")

        # Proceed with your code here

    except mysql.connector.Error as e:
        print("Error connecting to MySQL database:", e)
    
    try:
        cursor = mydb.cursor(dictionary=True)
        query = """
        USE sakila;

        SELECT 
            c.first_name AS 'First Name', 
            c.last_name AS 'Last Name', 
            c.email AS 'Email', 
            ci.city AS 'City', 
            co.country AS 'Country', 
            ST_X(a.location) AS 'Longitude', 
            ST_Y(a.location) AS 'Latitude', 
            c.active AS 'Active Status', 
            MAX(r.rental_date) AS 'Last Rental Date', 
            (SELECT f.title FROM inventory i 
            JOIN film f ON i.film_id = f.film_id 
            JOIN rental r ON i.inventory_id = r.inventory_id
            WHERE r.customer_id = c.customer_id
            ORDER BY r.rental_date DESC
            LIMIT 1) AS 'Last Rental Film'
        FROM 
            customer c
        JOIN 
            address a ON c.address_id = a.address_id
        JOIN 
            city ci ON a.city_id = ci.city_id
        JOIN 
            country co ON ci.country_id = co.country_id
        LEFT JOIN 
            rental r ON c.customer_id = r.customer_id
        GROUP BY 
            c.customer_id, c.first_name, c.last_name, c.email, ci.city, co.country, ST_X(a.location), ST_Y(a.location), c.active
        ORDER BY 
            MAX(r.rental_date) DESC;
        """
        print("SQL GOING THROUGH", file=sys.stderr)
        cursor.execute(query)
        customers = cursor.fetchall()
        # customers = [row._asdict() for row in customers]
        print(customers)
        print('HELLO world')
        cursor.close()
        mydb.close()
        return render_template('HomePage.html', contributors=contributors, tasks=tasks, customers=customers)
    except mysql.connector.Error as error:
        print("ERROR DOING THE QUERY")
        print('YUH!', file=sys.stderr)
        return "ERROR has occured"



if __name__ == '__main__':
    app.run(debug=True)