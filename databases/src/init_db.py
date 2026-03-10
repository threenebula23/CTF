import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Создаем таблицу пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            is_admin BOOLEAN DEFAULT 0
        )
    ''')
    
    # Добавляем тестовых пользователей
    cursor.execute("INSERT OR IGNORE INTO users (id, username, password, is_admin) VALUES (1, 'admin', 'super_secret_password_123', 1)")
    cursor.execute("INSERT OR IGNORE INTO users (id, username, password, is_admin) VALUES (2, 'user', 'password', 0)")
    
    conn.commit()
    conn.close()
    print('База данных инициализирована.')

if __name__ == '__main__':
    init_db()