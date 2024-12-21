from flask import Flask, request, jsonify, send_file, make_response
from datetime import datetime
import os

app = Flask(__name__)

# Хранилище для заметок
notes = {}
# Пользователи для авторизации
users = {"admin": "password123"}

# Проверка авторизации
@app.before_request
def check_auth():
    if request.endpoint != 'login' and 'user' not in request.cookies:
        return jsonify({"error": "Unauthorized. Please log in."}), 401

@app.route('/login', methods=['POST'])
def login():
    """Авторизация пользователя"""
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Invalid input"}), 400

    username = data['username']
    password = data['password']

    if username in users and users[username] == password:
        response = make_response(jsonify({"message": "Login successful"}))
        response.set_cookie('user', username)
        return response
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route('/logout', methods=['POST'])
def logout():
    """Выход пользователя"""
    response = make_response(jsonify({"message": "Logged out"}))
    response.delete_cookie('user')
    return response

@app.route('/api/notes', methods=['GET'])
def list_notes():
    """Возвращает список всех заметок"""
    return jsonify(notes)

@app.route('/api/notes', methods=['POST'])
def create_note():
    """Создает новую заметку"""
    data = request.get_json()
    if not data or 'name' not in data or 'content' not in data:
        return jsonify({"error": "Invalid input"}), 400

    note_id = len(notes) + 1
    notes[note_id] = {
        'name': data['name'],
        'content': data['content'],
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return jsonify({"message": "Note created", "note_id": note_id}), 201

@app.route('/api/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    """Возвращает одну заметку по ID"""
    note = notes.get(note_id)
    if not note:
        return jsonify({"error": "Note not found"}), 404
    return jsonify(note)

@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    """Удаляет заметку по ID"""
    if note_id in notes:
        del notes[note_id]
        return jsonify({"message": "Note deleted"}), 200
    else:
        return jsonify({"error": "Note not found"}), 404

@app.route('/api/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    """Обновляет заметку по ID"""
    note = notes.get(note_id)
    if not note:
        return jsonify({"error": "Note not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400

    note['name'] = data.get('name', note['name'])
    note['content'] = data.get('content', note['content'])
    note['date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return jsonify({"message": "Note updated", "note": note}), 200

@app.route('/downloadall', methods=['GET'])
def download_all_notes():
    """Создает файл со всеми заметками и позволяет скачать его"""
    if not notes:
        return jsonify({"error": "No notes available"}), 404

    file_path = 'notes.txt'
    with open(file_path, 'w', encoding='utf-8') as file:
        for note_id, note in notes.items():
            file.write(f"ID: {note_id}\n")
            file.write(f"Name: {note['name']}\n")
            file.write(f"Content: {note['content']}\n")
            file.write(f"Date: {note['date']}\n")
            file.write("-" * 40 + "\n")

    return send_file(file_path, as_attachment=True, download_name='notes.txt')

if __name__ == '__main__':
    app.run()
