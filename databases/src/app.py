from flask import Flask, request, render_template, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def get_db_connection():
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # УЯЗВИМЫЙ ЗАПРОС: Использование f-строк для формирования SQL-запроса
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    print(f"Executing query: {query}")
    conn = get_db_connection()
    user = conn.execute(query).fetchone()
    conn.close()
    if user:
        flash(f'Успешный вход! Добро пожаловать, {user["username"]}.', 'success')
        if user['is_admin']:
            flash('Вы вошли как администратор!', 'info')
            return redirect(url_for('index'))
        else:
            flash('Неверное имя пользователя или пароль.', 'danger')
            return redirect(url_for('index'))
        
if __name__ == '__main__':
    # Убедимся, что БД существует
    if not os.path.exists('database.db'):
        from init_db import init_db
        init_db()  
    app.run(debug=True, port=8001)