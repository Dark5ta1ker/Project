from app import create_app
import os

# Определяем среду выполнения
env = os.getenv('FLASK_ENV', 'development')

app = create_app(env)

if __name__ == '__main__':
    with app.app_context():
        from app.models import db
        if env == 'development':
            db.create_all()  # Создаем таблицы только в dev-режиме
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG'],
        use_reloader=False  # ← вот это ключ
    )