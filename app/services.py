def insert_grades(conn, df):
    cur = conn.cursor()
    inserted = 0
    for _, row in df.iterrows():
        cur.execute(
            "INSERT INTO grades (date, group_number, full_name, grade) VALUES (%s, %s, %s, %s)",
            (row['Дата'], row['Номер группы'], row['ФИО'], row['Оценка'])
        )
        inserted += 1
    conn.commit()
    cur.execute("SELECT COUNT(DISTINCT full_name) FROM grades")
    students = cur.fetchone()['count']
    cur.close()
    return inserted, students

def get_students_with_twos_condition(conn, operator, threshold):
    cur = conn.cursor()
    query = f"""
        SELECT full_name, COUNT(*) as count_twos
        FROM grades
        WHERE grade = 2
        GROUP BY full_name
        HAVING COUNT(*) {operator} %s
        ORDER BY full_name
    """
    cur.execute(query, (threshold,))
    results = cur.fetchall()
    cur.close()
    return results