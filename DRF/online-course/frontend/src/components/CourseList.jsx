import { useEffect, useState } from "react";
import api from "../api";
import CourseForm from "./CourseForm";
import CourseFilter from "./CourseFilter";

function CourseList() {
  const [courses, setCourses] = useState([]);
  const [editingCourse, setEditingCourse] = useState(null);

  const fetchCourses = (instructorId = "") => {
    let url = "courses/";
    if (instructorId) url += `?instructor_id=${instructorId}`;
    api.get(url).then(res => setCourses(res.data));
  };

  useEffect(() => { fetchCourses(); }, []);

  const handleDelete = (id) => {
    if (window.confirm("Are you sure you want to delete?")) {
      api.delete(`courses/${id}/`).then(() => fetchCourses());
    }
  };

  const handleEdit = (course) => { setEditingCourse(course); };
  const handleUpdated = () => { setEditingCourse(null); fetchCourses(); };

  return (
    <div className="bg-gray-50 p-6 rounded-lg shadow-md mb-6">
      <h2 className="text-2xl font-bold mb-4 text-gray-800">Courses</h2>

      {/* Filter dropdown */}
      <div className="mb-4">
        <CourseFilter onFilter={fetchCourses} />
      </div>

      {/* Edit Form */}
      {editingCourse && (
        <CourseForm course={editingCourse} onAdded={handleUpdated} />
      )}

      {/* Course List */}
      <ul className="space-y-3">
        {courses.map(c => (
          <li
            key={c.id}
            className="flex justify-between items-center bg-white p-4 rounded-lg shadow-sm hover:shadow-md transition"
          >
            <span className="text-gray-700 font-medium">
              <strong>{c.title}</strong> ({c.total_lessons} lessons) - {c.instructor?.name}
            </span>
            <div className="flex gap-2">
              <button
                className="bg-yellow-400 text-white px-3 py-1 rounded hover:bg-yellow-500 transition"
                onClick={() => handleEdit(c)}
              >
                Edit
              </button>
              <button
                className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600 transition"
                onClick={() => handleDelete(c.id)}
              >
                Delete
              </button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default CourseList;
