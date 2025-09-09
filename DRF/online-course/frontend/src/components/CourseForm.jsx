import { useState, useEffect } from "react";
import api from "../api";

function CourseForm({ onAdded, course }) {
  const [title, setTitle] = useState(course ? course.title : "");
  const [description, setDescription] = useState(course ? course.description : "");
  const [instructorId, setInstructorId] = useState(course ? course.instructor.id : "");
  const [instructors, setInstructors] = useState([]);

  useEffect(() => {
    api.get("instructors/").then(res => setInstructors(res.data));
  }, []);

  useEffect(() => {
    if (course) {
      setTitle(course.title);
      setDescription(course.description);
      setInstructorId(course.instructor.id);
    }
  }, [course]);

  const handleSubmit = (e) => {
    e.preventDefault();
    const payload = { title, description, instructor_id: instructorId };
    if (course) {
      // Update
      api.put(`courses/${course.id}/`, payload)
        .then(res => onAdded && onAdded())
        .catch(err => console.error(err));
    } else {
      // Create
      api.post("courses/", payload)
        .then(res => {
          setTitle("");
          setDescription("");
          setInstructorId("");
          onAdded && onAdded();
        })
        .catch(err => console.error(err));
    }
  };

  return (
    <div className="bg-white p-4 rounded-lg shadow-md mb-4 w-full max-w-md">
      <h2 className="text-xl font-bold mb-3 text-gray-800">
        {course ? "Edit Course" : "Add Course"}
      </h2>
      <form className="flex flex-col gap-3" onSubmit={handleSubmit}>
        <input
          className="border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
          placeholder="Title"
          value={title}
          onChange={e => setTitle(e.target.value)}
          required
        />
        <input
          className="border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
          placeholder="Description"
          value={description}
          onChange={e => setDescription(e.target.value)}
        />
        <select
          className="border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
          value={instructorId}
          onChange={e => setInstructorId(e.target.value)}
          required
        >
          <option value="">Select Instructor</option>
          {instructors.map(ins => (
            <option key={ins.id} value={ins.id}>{ins.name}</option>
          ))}
        </select>
        <button
          className="bg-blue-500 text-white p-2 rounded hover:bg-blue-600 transition"
          type="submit"
        >
          {course ? "Update" : "Add"}
        </button>
      </form>
    </div>
  );
}

export default CourseForm;
