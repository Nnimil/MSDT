from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Хранилище для заметок
notes = {}

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

if __name__ == '__main__':
    app.run(debug=True)
