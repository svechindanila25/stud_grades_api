import pytest
from fastapi.testclient import TestClient
from app.main import app
import io
client = TestClient(app)
good_csv = """Дата;Номер группы;ФИО;Оценка
11.03.2025;101Б;Курочкин Антон Владимирович;4
18.09.2024;102Б;Москвичев Андрей;3
26.09.2024;103М;Фомин Глеб Александрович;4
"""
bad_grade_csv = """Дата;Номер группы;ФИО;Оценка
11.03.2025;101Б;Курочкин Антон Владимирович;6
"""

# CSV с неправильной датой
bad_date_csv = """Дата;Номер группы;ФИО;Оценка
2025-03-11;101Б;Курочкин Антон Владимирович;4
"""

def test_upload_good_csv():
    response = client.post(
        "/upload-grades",
        files={"file": ("grades.csv", io.BytesIO(good_csv.encode()), "text/csv")}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["records_loaded"] == 3
    assert data["students"] == 3

def test_upload_bad_grade():
    response = client.post(
        "/upload-grades",
        files={"file": ("grades.csv", io.BytesIO(bad_grade_csv.encode()), "text/csv")}
    )
    assert response.status_code == 400
    assert "Grades must be between 2 and 5" in response.text

def test_upload_bad_date():
    response = client.post(
        "/upload-grades",
        files={"file": ("grades.csv", io.BytesIO(bad_date_csv.encode()), "text/csv")}
    )
    assert response.status_code == 400
    assert "Invalid date format" in response.text