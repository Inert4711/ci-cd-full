from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def index():
    """Главная страница"""
    return jsonify({
        "message": "Welcome to CI/CD Demo App!",
        "status": "ok",
        "version": "1.0.0"
    })

@app.route('/api/health')
def health():
    """Эндпоинт для проверки здоровья сервиса"""
    return jsonify({
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": "2026-03-13T12:00:00Z"
    })

@app.route('/api/users')
def users():
    """Список пользователей"""
    return jsonify({
        "users": [
            {"id": 1, "name": "Alice", "role": "admin"},
            {"id": 2, "name": "Bob", "role": "user"}
        ],
        "total": 2
    })

@app.route('/api/users/<int:user_id>')
def get_user(user_id):
    """Получить пользователя по ID"""
    users = {
        1: {"id": 1, "name": "Alice", "role": "admin"},
        2: {"id": 2, "name": "Bob", "role": "user"}
    }
    user = users.get(user_id)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)