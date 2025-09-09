import { useEffect, useState } from "react";
import api from "../api";
import InstructorForm from "./InstructorForm";

function InstructorList() {
  const [instructors, setInstructors] = useState([]);
  const [editingInstructor, setEditingInstructor] = useState(null);

  const fetchInstructors = () => {
    api.get("instructors/").then(res => setInstructors(res.data));
  };

  useEffect(() => {
    fetchInstructors();
  }, []);

  const handleDelete = (id) => {
    if (window.confirm("Are you sure you want to delete?")) {
      api.delete(`instructors/${id}/`).then(() => fetchInstructors());
    }
  };

  const handleEdit = (instructor) => {
    setEditingInstructor(instructor);
  };

  const handleUpdated = () => {
    setEditingInstructor(null);
    fetchInstructors();
  };

  return (
    <div className="bg-gray-50 p-6 rounded-lg shadow-md mb-6">
      <h2 className="text-2xl font-bold mb-4 text-gray-800">Instructors</h2>

      {/* Edit Form */}
      {editingInstructor && (
        <InstructorForm
          instructor={editingInstructor}
          onAdded={handleUpdated}
        />
      )}

      {/* Instructor List */}
      <ul className="space-y-3">
        {instructors.map(ins => (
          <li
            key={ins.id}
            className="flex justify-between items-center bg-white p-4 rounded-lg shadow-sm hover:shadow-md transition"
          >
            <span className="text-gray-700 font-medium">
              {ins.name} ({ins.email})
            </span>
            <div className="flex gap-2">
              <button
                className="bg-yellow-400 text-white px-3 py-1 rounded hover:bg-yellow-500 transition"
                onClick={() => handleEdit(ins)}
              >
                Edit
              </button>
              <button
                className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600 transition"
                onClick={() => handleDelete(ins.id)}
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

export default InstructorList;
