from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import os

app = FastAPI(
    title="Student Management System API",
    version="1.0.0"
)

# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# DATABASE
# =========================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "db.sqlite3")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# =========================
# MODELS
# =========================

class Student(BaseModel):
    name: str
    student_id: str
    email: str
    phone: str
    course: str
    date_of_birth: str | None = None


class Course(BaseModel):
    name: str
    code: str
    teacher_id: int | None = None


class Teacher(BaseModel):
    name: str
    teacher_id: str
    email: str
    phone: str


class Result(BaseModel):
    marks: float
    grade: str
    course_id: int
    student_id: int


class Attendance(BaseModel):
    date: str
    present: bool
    course_id: int
    student_id: int


# =========================
# HOME
# =========================

@app.get("/")
def home():
    return {
        "message": "Student Management System API is running"
    }


# =========================
# DASHBOARD
# =========================

@app.get("/api/dashboard")
def dashboard():

    conn = get_db()

    try:
        students = conn.execute(
            "SELECT COUNT(*) FROM students_student"
        ).fetchone()[0]

        courses = conn.execute(
            "SELECT COUNT(*) FROM students_course"
        ).fetchone()[0]

        teachers = conn.execute(
            "SELECT COUNT(*) FROM students_teacher"
        ).fetchone()[0]

        results = conn.execute(
            "SELECT COUNT(*) FROM students_result"
        ).fetchone()[0]

        attendance = conn.execute(
            "SELECT COUNT(*) FROM students_attendance"
        ).fetchone()[0]

        return {
            "students": students,
            "courses": courses,
            "teachers": teachers,
            "results": results,
            "attendance": attendance
        }

    finally:
        conn.close()


# =========================
# STUDENTS
# =========================

@app.get("/api/students")
def get_students():

    conn = get_db()

    try:
        rows = conn.execute(
            """
            SELECT
                id,
                name,
                student_id,
                email,
                phone,
                course,
                date_of_birth
            FROM students_student
            ORDER BY id
            """
        ).fetchall()

        return [dict(row) for row in rows]

    finally:
        conn.close()


@app.post("/api/students")
def add_student(student: Student):

    conn = get_db()

    try:
        cursor = conn.execute(
            """
            INSERT INTO students_student
            (name, student_id, email, phone, course, date_of_birth)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                student.name,
                student.student_id,
                student.email,
                student.phone,
                student.course,
                student.date_of_birth
            )
        )

        conn.commit()

        return {
            "message": "Student added successfully",
            "id": cursor.lastrowid
        }

    finally:
        conn.close()


@app.put("/api/students/{student_id}")
def update_student(student_id: int, student: Student):

    conn = get_db()

    try:
        cursor = conn.execute(
            """
            UPDATE students_student
            SET
                name = ?,
                student_id = ?,
                email = ?,
                phone = ?,
                course = ?,
                date_of_birth = ?
            WHERE id = ?
            """,
            (
                student.name,
                student.student_id,
                student.email,
                student.phone,
                student.course,
                student.date_of_birth,
                student_id
            )
        )

        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Student not found"
            )

        return {
            "message": "Student updated successfully"
        }

    finally:
        conn.close()


@app.delete("/api/students/{student_id}")
def delete_student(student_id: int):

    conn = get_db()

    try:
        cursor = conn.execute(
            "DELETE FROM students_student WHERE id = ?",
            (student_id,)
        )

        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Student not found"
            )

        return {
            "message": "Student deleted successfully"
        }

    finally:
        conn.close()


# =========================
# COURSES
# =========================

@app.get("/api/courses")
def get_courses():

    conn = get_db()

    try:
        rows = conn.execute(
            """
            SELECT
                c.id,
                c.name,
                c.code,
                c.teacher_id,
                t.name AS teacher_name
            FROM students_course c
            LEFT JOIN students_teacher t
                ON c.teacher_id = t.id
            ORDER BY c.id
            """
        ).fetchall()

        return [dict(row) for row in rows]

    finally:
        conn.close()


@app.post("/api/courses")
def add_course(course: Course):

    conn = get_db()

    try:
        cursor = conn.execute(
            """
            INSERT INTO students_course
            (name, code, teacher_id)
            VALUES (?, ?, ?)
            """,
            (
                course.name,
                course.code,
                course.teacher_id
            )
        )

        conn.commit()

        return {
            "message": "Course added successfully",
            "id": cursor.lastrowid
        }

    finally:
        conn.close()


@app.delete("/api/courses/{course_id}")
def delete_course(course_id: int):

    conn = get_db()

    try:
        cursor = conn.execute(
            "DELETE FROM students_course WHERE id = ?",
            (course_id,)
        )

        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Course not found"
            )

        return {
            "message": "Course deleted successfully"
        }

    finally:
        conn.close()


# =========================
# TEACHERS
# =========================

@app.get("/api/teachers")
def get_teachers():

    conn = get_db()

    try:
        rows = conn.execute(
            """
            SELECT
                id,
                name,
                teacher_id,
                email,
                phone
            FROM students_teacher
            ORDER BY id
            """
        ).fetchall()

        return [dict(row) for row in rows]

    finally:
        conn.close()


@app.post("/api/teachers")
def add_teacher(teacher: Teacher):

    conn = get_db()

    try:
        cursor = conn.execute(
            """
            INSERT INTO students_teacher
            (name, teacher_id, email, phone)
            VALUES (?, ?, ?, ?)
            """,
            (
                teacher.name,
                teacher.teacher_id,
                teacher.email,
                teacher.phone
            )
        )

        conn.commit()

        return {
            "message": "Teacher added successfully",
            "id": cursor.lastrowid
        }

    finally:
        conn.close()


@app.delete("/api/teachers/{teacher_id}")
def delete_teacher(teacher_id: int):

    conn = get_db()

    try:
        cursor = conn.execute(
            "DELETE FROM students_teacher WHERE id = ?",
            (teacher_id,)
        )

        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Teacher not found"
            )

        return {
            "message": "Teacher deleted successfully"
        }

    finally:
        conn.close()


# =========================
# RESULTS
# =========================

@app.get("/api/results")
def get_results():

    conn = get_db()

    try:
        rows = conn.execute(
            """
            SELECT
                r.id,
                r.marks,
                r.grade,
                r.course_id,
                r.student_id,
                s.name AS student_name,
                c.name AS course_name
            FROM students_result r
            LEFT JOIN students_student s
                ON r.student_id = s.id
            LEFT JOIN students_course c
                ON r.course_id = c.id
            ORDER BY r.id
            """
        ).fetchall()

        return [dict(row) for row in rows]

    finally:
        conn.close()


@app.post("/api/results")
def add_result(result: Result):

    conn = get_db()

    try:
        cursor = conn.execute(
            """
            INSERT INTO students_result
            (marks, grade, course_id, student_id)
            VALUES (?, ?, ?, ?)
            """,
            (
                result.marks,
                result.grade,
                result.course_id,
                result.student_id
            )
        )

        conn.commit()

        return {
            "message": "Result added successfully",
            "id": cursor.lastrowid
        }

    finally:
        conn.close()


# =========================
# ATTENDANCE
# =========================

@app.get("/api/attendance")
def get_attendance():

    conn = get_db()

    try:
        rows = conn.execute(
            """
            SELECT
                a.id,
                a.date,
                a.present,
                a.course_id,
                a.student_id,
                s.name AS student_name,
                c.name AS course_name
            FROM students_attendance a
            LEFT JOIN students_student s
                ON a.student_id = s.id
            LEFT JOIN students_course c
                ON a.course_id = c.id
            ORDER BY a.date DESC, a.id DESC
            """
        ).fetchall()

        return [dict(row) for row in rows]

    finally:
        conn.close()


@app.post("/api/attendance")
def add_attendance(attendance: Attendance):

    conn = get_db()

    try:
        cursor = conn.execute(
            """
            INSERT INTO students_attendance
            (date, present, course_id, student_id)
            VALUES (?, ?, ?, ?)
            """,
            (
                attendance.date,
                attendance.present,
                attendance.course_id,
                attendance.student_id
            )
        )

        conn.commit()

        return {
            "message": "Attendance added successfully",
            "id": cursor.lastrowid
        }

    finally:
        conn.close()