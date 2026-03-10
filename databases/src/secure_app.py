from flask import Flask, request, render_template, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey_secure'

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
    
    # БЕЗОПАСНЫЙ ЗАПРОС: Использование параметризации (?)
    # Это предотвращает SQL-инъекции, так как драйвер БД сам экранирует данные
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    
    print(f"Executing secure query with params: {username}, {password}")
    
    conn = get_db_connection()
    user = conn.execute(query, (username, password)).fetchone()
    conn.close()
    
    if user:
        flash(f'Успешный вход! Добро пожаловать, {user["username"]}.', 'success')
        return redirect(url_for('index'))
    else:
        flash('Неверное имя пользователя или пароль.', 'danger')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=8002)