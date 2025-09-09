import { useEffect, useState } from "react";
import api from "../api";

function CourseFilter({ onFilter }) {
  const [instructors, setInstructors] = useState([]);
  const [selectedInstructor, setSelectedInstructor] = useState("");

  useEffect(() => {
    api.get("instructors/").then(res => setInstructors(res.data));
  }, []);

  const handleChange = (e) => {
    const instructorId = e.target.value;
    setSelectedInstructor(instructorId);
    onFilter(instructorId);
  };

  return (
    <div className="mb-4">
      <label className="block mb-1 text-gray-700 font-medium">Filter by Instructor:</label>
      <select
        className="border border-gray-300 p-2 rounded w-full max-w-xs focus:outline-none focus:ring-2 focus:ring-blue-400"
        value={selectedInstructor}
        onChange={handleChange}
      >
        <option value="">All</option>
        {instructors.map(i => (
          <option key={i.id} value={i.id}>{i.name}</option>
        ))}
      </select>
    </div>
  );
}

export default CourseFilter;
