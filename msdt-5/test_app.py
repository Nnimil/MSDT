import pytest
from app import app, notes
from datetime import datetime
from unittest.mock import patch

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# 1. Тест на получение списка заметок
def test_get_all_notes(client):
    notes.clear()
    notes[1] = {"name": "Test Note", "content": "Test Content", "date": "2024-12-22"}
    response = client.get('/api/notes')
    assert response.status_code == 200
    assert response.json == {"1": notes[1]}

# 2. Тест на создание новой заметки
def test_create_note_success(client):
    notes.clear()
    response = client.post('/api/notes', json={"name": "New Note", "content": "Note Content"})
    assert response.status_code == 201
    assert response.json["message"] == "Note created"
    assert "note_id" in response.json
    note_id = response.json["note_id"]
    assert notes[note_id]["name"] == "New Note"
    assert notes[note_id]["content"] == "Note Content"

# 3. Тест на создание заметки с некорректными данными (параметризация)
@pytest.mark.parametrize("data, expected_status, expected_message", [
    ({"name": ""}, 400, "Invalid input"),
    ({"content": "No name provided"}, 400, "Invalid input"),
    ({}, 400, "Invalid input")
])
def test_create_note_invalid_data(client, data, expected_status, expected_message):
    response = client.post('/api/notes', json=data)
    assert response.status_code == expected_status
    assert response.json["error"] == expected_message

# 4. Тест на получение заметки по ID
def test_get_note_by_id(client):
    notes.clear()
    notes[1] = {"name": "Test Note", "content": "Test Content", "date": "2024-12-22"}
    response = client.get('/api/notes/1')
    assert response.status_code == 200
    assert response.json == notes[1]

# 5. Тест на получение несуществующей заметки
def test_get_nonexistent_note_by_id(client):
    notes.clear()
    response = client.get('/api/notes/99')
    assert response.status_code == 404
    assert response.json["error"] == "Note not found"

# 6. Тест с мокированием даты при создании заметки
@patch("app.datetime")
def test_create_note_with_mocked_date(mock_datetime, client):
    mock_datetime.now.return_value = datetime(2024, 12, 25, 15, 30)
    response = client.post('/api/notes', json={"name": "Mocked Note", "content": "Mocked Content"})
    assert response.status_code == 201
    note_id = response.json["note_id"]
    assert notes[note_id]["date"] == "2024-12-25 15:30:00"

# 7. Тест на обновление заметки
def test_update_note_success(client):
    notes.clear()
    notes[1] = {"name": "Old Note", "content": "Old Content", "date": "2024-12-22"}
    response = client.put('/api/notes/1', json={"name": "Updated Note", "content": "Updated Content"})
    assert response.status_code == 200
    assert response.json["message"] == "Note updated"
    assert notes[1]["name"] == "Updated Note"
    assert notes[1]["content"] == "Updated Content"

# 8. Тест на удаление заметки
def test_delete_note_success(client):
    notes.clear()
    notes[1] = {"name": "Note to Delete", "content": "Content", "date": "2024-12-22"}
    response = client.delete('/api/notes/1')
    assert response.status_code == 200
    assert response.json["message"] == "Note deleted"
    assert 1 not in notes

# 9. Тест на удаление несуществующей заметки
def test_delete_nonexistent_note(client):
    notes.clear()
    response = client.delete('/api/notes/99')
    assert response.status_code == 404
    assert response.json["error"] == "Note not found"
