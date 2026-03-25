from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
from io import StringIO
from app.database import get_db_connection
from app.services import insert_grades, get_students_with_twos_condition

app = FastAPI(title="Student Grades API")

@app.post("/upload-grades")
async def upload_grades(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    contents = await file.read()
    try:
        df = pd.read_csv(StringIO(contents.decode('utf-8-sig')), sep=';')
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading CSV: {str(e)}")

    df.columns = df.columns.str.replace('\ufeff', '').str.strip()

    required_columns = ['Дата', 'Номер группы', 'ФИО', 'Оценка']
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required columns: {missing}. Found: {list(df.columns)}"
        )
    if not df['Оценка'].between(2, 5).all():
        raise HTTPException(status_code=400, detail="Grades must be between 2 and 5")
    try:
        df['Дата'] = pd.to_datetime(df['Дата'], format='%d.%m.%Y', errors='raise').dt.date
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format. Expected dd.mm.yyyy. Error: {str(e)}")
    conn = get_db_connection()
    try:
        records_loaded, students = insert_grades(conn, df)
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()
    return {
        "status": "ok",
        "records_loaded": records_loaded,
        "students": students
    }

@app.get("/students/more-than-3-twos")
async def more_than_3_twos():
    conn = get_db_connection()
    try:
        result = get_students_with_twos_condition(conn, '>', 3)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()
    return result

@app.get("/students/less-than-5-twos")
async def less_than_5_twos():
    conn = get_db_connection()
    try:
        result = get_students_with_twos_condition(conn, '<', 5)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()
    return result