import { useEffect, useState } from "react";
import "./App.css";

const API = "http://127.0.0.1:8000/api";

function App() {
  const [page, setPage] = useState("Dashboard");

  const [students, setStudents] = useState([]);
  const [courses, setCourses] = useState([]);
  const [teachers, setTeachers] = useState([]);
  const [results, setResults] = useState([]);
  const [attendance, setAttendance] = useState([]);
  const [dashboard, setDashboard] = useState({});

  const [studentForm, setStudentForm] = useState({
    name: "",
    student_id: "",
    email: "",
    phone: "",
    course: "",
    date_of_birth: "",
  });

  const [editingStudent, setEditingStudent] = useState(null);

  const [courseForm, setCourseForm] = useState({
    name: "",
    code: "",
    teacher_id: "",
  });

  const [teacherForm, setTeacherForm] = useState({
    name: "",
    teacher_id: "",
    email: "",
    phone: "",
  });

  const [resultForm, setResultForm] = useState({
    marks: "",
    grade: "",
    course_id: "",
    student_id: "",
  });

  const [attendanceForm, setAttendanceForm] = useState({
    date: "",
    present: true,
    course_id: "",
    student_id: "",
  });

  const loadData = async () => {
    try {
      const [
        dash,
        studentData,
        courseData,
        teacherData,
        resultData,
        attendanceData,
      ] = await Promise.all([
        fetch(`${API}/dashboard`).then((r) => r.json()),
        fetch(`${API}/students`).then((r) => r.json()),
        fetch(`${API}/courses`).then((r) => r.json()),
        fetch(`${API}/teachers`).then((r) => r.json()),
        fetch(`${API}/results`).then((r) => r.json()),
        fetch(`${API}/attendance`).then((r) => r.json()),
      ]);

      setDashboard(dash);
      setStudents(studentData);
      setCourses(courseData);
      setTeachers(teacherData);
      setResults(resultData);
      setAttendance(attendanceData);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const request = async (url, method, data = null) => {
    const options = {
      method,
      headers: {
        "Content-Type": "application/json",
      },
    };

    if (data) {
      options.body = JSON.stringify(data);
    }

    const response = await fetch(url, options);

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Request failed");
    }

    return response.json();
  };

  // STUDENTS

  const submitStudent = async (e) => {
    e.preventDefault();

    try {
      if (editingStudent) {
        await request(
          `${API}/students/${editingStudent}`,
          "PUT",
          studentForm
        );
      } else {
        await request(`${API}/students`, "POST", studentForm);
      }

      setStudentForm({
        name: "",
        student_id: "",
        email: "",
        phone: "",
        course: "",
        date_of_birth: "",
      });

      setEditingStudent(null);
      loadData();
    } catch (error) {
      alert(error.message);
    }
  };

  const editStudent = (student) => {
    setEditingStudent(student.id);

    setStudentForm({
      name: student.name,
      student_id: student.student_id,
      email: student.email,
      phone: student.phone,
      course: student.course,
      date_of_birth: student.date_of_birth || "",
    });
  };

  const deleteStudent = async (id) => {
    if (!window.confirm("Delete this student?")) return;

    try {
      await request(`${API}/students/${id}`, "DELETE");
      loadData();
    } catch (error) {
      alert(error.message);
    }
  };

  // COURSE

  const submitCourse = async (e) => {
    e.preventDefault();

    try {
      await request(`${API}/courses`, "POST", {
        name: courseForm.name,
        code: courseForm.code,
        teacher_id: courseForm.teacher_id
          ? Number(courseForm.teacher_id)
          : null,
      });

      setCourseForm({
        name: "",
        code: "",
        teacher_id: "",
      });

      loadData();
    } catch (error) {
      alert(error.message);
    }
  };

  const deleteCourse = async (id) => {
    if (!window.confirm("Delete this course?")) return;

    try {
      await request(`${API}/courses/${id}`, "DELETE");
      loadData();
    } catch (error) {
      alert(error.message);
    }
  };

  // TEACHER

  const submitTeacher = async (e) => {
    e.preventDefault();

    try {
      await request(`${API}/teachers`, "POST", teacherForm);

      setTeacherForm({
        name: "",
        teacher_id: "",
        email: "",
        phone: "",
      });

      loadData();
    } catch (error) {
      alert(error.message);
    }
  };

  const deleteTeacher = async (id) => {
    if (!window.confirm("Delete this teacher?")) return;

    try {
      await request(`${API}/teachers/${id}`, "DELETE");
      loadData();
    } catch (error) {
      alert(error.message);
    }
  };

  // RESULT

  const submitResult = async (e) => {
    e.preventDefault();

    try {
      await request(`${API}/results`, "POST", {
        marks: Number(resultForm.marks),
        grade: resultForm.grade,
        course_id: Number(resultForm.course_id),
        student_id: Number(resultForm.student_id),
      });

      setResultForm({
        marks: "",
        grade: "",
        course_id: "",
        student_id: "",
      });

      loadData();
    } catch (error) {
      alert(error.message);
    }
  };

  // ATTENDANCE

  const submitAttendance = async (e) => {
    e.preventDefault();

    try {
      await request(`${API}/attendance`, "POST", {
        date: attendanceForm.date,
        present: attendanceForm.present,
        course_id: Number(attendanceForm.course_id),
        student_id: Number(attendanceForm.student_id),
      });

      setAttendanceForm({
        date: "",
        present: true,
        course_id: "",
        student_id: "",
      });

      loadData();
    } catch (error) {
      alert(error.message);
    }
  };

  return (
    <div className="app">

      <aside className="sidebar">

        <div className="logo">
          <div className="logo-icon">S</div>

          <div>
            <h2>StudentHub</h2>
            <p>Management System</p>
          </div>
        </div>

        <nav>
          {[
            "Dashboard",
            "Students",
            "Courses",
            "Teachers",
            "Results",
            "Attendance",
          ].map((item) => (
            <div
              key={item}
              className={`nav-item ${
                page === item ? "active" : ""
              }`}
              onClick={() => setPage(item)}
            >
              {item}
            </div>
          ))}
        </nav>

        <div className="sidebar-footer">
          FastAPI + React
        </div>

      </aside>

      <main className="main">

        <header className="topbar">
          <div>
            <h1>{page}</h1>
            <p>Student Management System</p>
          </div>
        </header>


        {/* DASHBOARD */}

        {page === "Dashboard" && (
          <>
            <div className="stats-grid">

              <div className="stat-card">
                <span>Students</span>
                <strong>{dashboard.students || 0}</strong>
              </div>

              <div className="stat-card">
                <span>Courses</span>
                <strong>{dashboard.courses || 0}</strong>
              </div>

              <div className="stat-card">
                <span>Teachers</span>
                <strong>{dashboard.teachers || 0}</strong>
              </div>

              <div className="stat-card">
                <span>Results</span>
                <strong>{dashboard.results || 0}</strong>
              </div>

              <div className="stat-card">
                <span>Attendance</span>
                <strong>{dashboard.attendance || 0}</strong>
              </div>

            </div>

            <section className="card welcome-card">
              <h2>Welcome to StudentHub 👋</h2>
              <p>
                Manage students, courses, teachers,
                results and attendance from one place.
              </p>
            </section>
          </>
        )}


        {/* STUDENTS */}

        {page === "Students" && (
          <>
            <section className="card">

              <div className="section-title">
                <div>
                  <h2>
                    {editingStudent
                      ? "Edit Student"
                      : "Add Student"}
                  </h2>
                  <p>Student information</p>
                </div>
              </div>

              <form
                className="student-form"
                onSubmit={submitStudent}
              >

                <input
                  placeholder="Name"
                  value={studentForm.name}
                  onChange={(e) =>
                    setStudentForm({
                      ...studentForm,
                      name: e.target.value,
                    })
                  }
                  required
                />

                <input
                  placeholder="Student ID"
                  value={studentForm.student_id}
                  onChange={(e) =>
                    setStudentForm({
                      ...studentForm,
                      student_id: e.target.value,
                    })
                  }
                  required
                />

                <input
                  type="email"
                  placeholder="Email"
                  value={studentForm.email}
                  onChange={(e) =>
                    setStudentForm({
                      ...studentForm,
                      email: e.target.value,
                    })
                  }
                  required
                />

                <input
                  placeholder="Phone"
                  value={studentForm.phone}
                  onChange={(e) =>
                    setStudentForm({
                      ...studentForm,
                      phone: e.target.value,
                    })
                  }
                  required
                />

                <input
                  placeholder="Course"
                  value={studentForm.course}
                  onChange={(e) =>
                    setStudentForm({
                      ...studentForm,
                      course: e.target.value,
                    })
                  }
                  required
                />

                <input
                  type="date"
                  value={studentForm.date_of_birth}
                  onChange={(e) =>
                    setStudentForm({
                      ...studentForm,
                      date_of_birth: e.target.value,
                    })
                  }
                />

                <button className="add-btn">
                  {editingStudent
                    ? "Update Student"
                    : "+ Add Student"}
                </button>

              </form>

            </section>

            <section className="card">
              <div className="section-title">
                <div>
                  <h2>Student Records</h2>
                  <p>{students.length} students</p>
                </div>
              </div>

              <div className="table-wrapper">
                <table>
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Name</th>
                      <th>Student ID</th>
                      <th>Email</th>
                      <th>Phone</th>
                      <th>Course</th>
                      <th>DOB</th>
                      <th>Actions</th>
                    </tr>
                  </thead>

                  <tbody>
                    {students.map((student) => (
                      <tr key={student.id}>
                        <td>#{student.id}</td>
                        <td><strong>{student.name}</strong></td>
                        <td>{student.student_id}</td>
                        <td>{student.email}</td>
                        <td>{student.phone}</td>
                        <td>{student.course}</td>
                        <td>{student.date_of_birth}</td>
                        <td>
                          <button
                            className="edit-btn"
                            onClick={() =>
                              editStudent(student)
                            }
                          >
                            Edit
                          </button>

                          <button
                            className="delete-btn"
                            onClick={() =>
                              deleteStudent(student.id)
                            }
                          >
                            Delete
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>
          </>
        )}


        {/* COURSES */}

        {page === "Courses" && (
          <>
            <section className="card">
              <div className="section-title">
                <h2>Add Course</h2>
              </div>

              <form
                className="student-form"
                onSubmit={submitCourse}
              >
                <input
                  placeholder="Course Name"
                  value={courseForm.name}
                  onChange={(e) =>
                    setCourseForm({
                      ...courseForm,
                      name: e.target.value,
                    })
                  }
                  required
                />

                <input
                  placeholder="Course Code"
                  value={courseForm.code}
                  onChange={(e) =>
                    setCourseForm({
                      ...courseForm,
                      code: e.target.value,
                    })
                  }
                  required
                />

                <select
                  value={courseForm.teacher_id}
                  onChange={(e) =>
                    setCourseForm({
                      ...courseForm,
                      teacher_id: e.target.value,
                    })
                  }
                >
                  <option value="">Select Teacher</option>

                  {teachers.map((teacher) => (
                    <option
                      key={teacher.id}
                      value={teacher.id}
                    >
                      {teacher.name}
                    </option>
                  ))}
                </select>

                <button className="add-btn">
                  + Add Course
                </button>
              </form>
            </section>

            <section className="card">
              <h2>Courses</h2>

              <div className="table-wrapper">
                <table>
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Name</th>
                      <th>Code</th>
                      <th>Teacher</th>
                      <th>Action</th>
                    </tr>
                  </thead>

                  <tbody>
                    {courses.map((course) => (
                      <tr key={course.id}>
                        <td>#{course.id}</td>
                        <td>{course.name}</td>
                        <td>{course.code}</td>
                        <td>
                          {course.teacher_name || "Not assigned"}
                        </td>
                        <td>
                          <button
                            className="delete-btn"
                            onClick={() =>
                              deleteCourse(course.id)
                            }
                          >
                            Delete
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>
          </>
        )}


        {/* TEACHERS */}

        {page === "Teachers" && (
          <>
            <section className="card">
              <h2>Add Teacher</h2>

              <form
                className="student-form"
                onSubmit={submitTeacher}
              >
                <input
                  placeholder="Name"
                  value={teacherForm.name}
                  onChange={(e) =>
                    setTeacherForm({
                      ...teacherForm,
                      name: e.target.value,
                    })
                  }
                  required
                />

                <input
                  placeholder="Teacher ID"
                  value={teacherForm.teacher_id}
                  onChange={(e) =>
                    setTeacherForm({
                      ...teacherForm,
                      teacher_id: e.target.value,
                    })
                  }
                  required
                />

                <input
                  type="email"
                  placeholder="Email"
                  value={teacherForm.email}
                  onChange={(e) =>
                    setTeacherForm({
                      ...teacherForm,
                      email: e.target.value,
                    })
                  }
                  required
                />

                <input
                  placeholder="Phone"
                  value={teacherForm.phone}
                  onChange={(e) =>
                    setTeacherForm({
                      ...teacherForm,
                      phone: e.target.value,
                    })
                  }
                  required
                />

                <button className="add-btn">
                  + Add Teacher
                </button>
              </form>
            </section>

            <section className="card">
              <h2>Teachers</h2>

              <div className="table-wrapper">
                <table>
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Name</th>
                      <th>Teacher ID</th>
                      <th>Email</th>
                      <th>Phone</th>
                      <th>Action</th>
                    </tr>
                  </thead>

                  <tbody>
                    {teachers.map((teacher) => (
                      <tr key={teacher.id}>
                        <td>#{teacher.id}</td>
                        <td>{teacher.name}</td>
                        <td>{teacher.teacher_id}</td>
                        <td>{teacher.email}</td>
                        <td>{teacher.phone}</td>
                        <td>
                          <button
                            className="delete-btn"
                            onClick={() =>
                              deleteTeacher(teacher.id)
                            }
                          >
                            Delete
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>
          </>
        )}


        {/* RESULTS */}

        {page === "Results" && (
          <>
            <section className="card">
              <h2>Add Result</h2>

              <form
                className="student-form"
                onSubmit={submitResult}
              >

                <select
                  value={resultForm.student_id}
                  onChange={(e) =>
                    setResultForm({
                      ...resultForm,
                      student_id: e.target.value,
                    })
                  }
                  required
                >
                  <option value="">Select Student</option>

                  {students.map((student) => (
                    <option
                      key={student.id}
                      value={student.id}
                    >
                      {student.name}
                    </option>
                  ))}
                </select>

                <select
                  value={resultForm.course_id}
                  onChange={(e) =>
                    setResultForm({
                      ...resultForm,
                      course_id: e.target.value,
                    })
                  }
                  required
                >
                  <option value="">Select Course</option>

                  {courses.map((course) => (
                    <option
                      key={course.id}
                      value={course.id}
                    >
                      {course.name}
                    </option>
                  ))}
                </select>

                <input
                  type="number"
                  placeholder="Marks"
                  value={resultForm.marks}
                  onChange={(e) =>
                    setResultForm({
                      ...resultForm,
                      marks: e.target.value,
                    })
                  }
                  required
                />

                <input
                  placeholder="Grade"
                  value={resultForm.grade}
                  onChange={(e) =>
                    setResultForm({
                      ...resultForm,
                      grade: e.target.value,
                    })
                  }
                  required
                />

                <button className="add-btn">
                  + Add Result
                </button>

              </form>
            </section>

            <section className="card">
              <h2>Results</h2>

              <div className="table-wrapper">
                <table>
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Student</th>
                      <th>Course</th>
                      <th>Marks</th>
                      <th>Grade</th>
                    </tr>
                  </thead>

                  <tbody>
                    {results.map((result) => (
                      <tr key={result.id}>
                        <td>#{result.id}</td>
                        <td>{result.student_name}</td>
                        <td>{result.course_name}</td>
                        <td>{result.marks}</td>
                        <td>{result.grade}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>
          </>
        )}


        {/* ATTENDANCE */}

        {page === "Attendance" && (
          <>
            <section className="card">
              <h2>Mark Attendance</h2>

              <form
                className="student-form"
                onSubmit={submitAttendance}
              >

                <select
                  value={attendanceForm.student_id}
                  onChange={(e) =>
                    setAttendanceForm({
                      ...attendanceForm,
                      student_id: e.target.value,
                    })
                  }
                  required
                >
                  <option value="">Select Student</option>

                  {students.map((student) => (
                    <option
                      key={student.id}
                      value={student.id}
                    >
                      {student.name}
                    </option>
                  ))}
                </select>

                <select
                  value={attendanceForm.course_id}
                  onChange={(e) =>
                    setAttendanceForm({
                      ...attendanceForm,
                      course_id: e.target.value,
                    })
                  }
                  required
                >
                  <option value="">Select Course</option>

                  {courses.map((course) => (
                    <option
                      key={course.id}
                      value={course.id}
                    >
                      {course.name}
                    </option>
                  ))}
                </select>

                <input
                  type="date"
                  value={attendanceForm.date}
                  onChange={(e) =>
                    setAttendanceForm({
                      ...attendanceForm,
                      date: e.target.value,
                    })
                  }
                  required
                />

                <select
                  value={attendanceForm.present}
                  onChange={(e) =>
                    setAttendanceForm({
                      ...attendanceForm,
                      present: e.target.value === "true",
                    })
                  }
                >
                  <option value="true">Present</option>
                  <option value="false">Absent</option>
                </select>

                <button className="add-btn">
                  + Mark Attendance
                </button>

              </form>
            </section>

            <section className="card">
              <h2>Attendance Records</h2>

              <div className="table-wrapper">
                <table>
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Date</th>
                      <th>Student</th>
                      <th>Course</th>
                      <th>Status</th>
                    </tr>
                  </thead>

                  <tbody>
                    {attendance.map((item) => (
                      <tr key={item.id}>
                        <td>#{item.id}</td>
                        <td>{item.date}</td>
                        <td>{item.student_name}</td>
                        <td>{item.course_name}</td>
                        <td>
                          {item.present
                            ? "Present"
                            : "Absent"}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>
          </>
        )}

      </main>
    </div>
  );
}

export default App;