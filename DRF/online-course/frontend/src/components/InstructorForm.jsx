import { useState, useEffect } from "react";
import api from "../api";

function InstructorForm({ onAdded, instructor }) {
  const [name, setName] = useState(instructor ? instructor.name : "");
  const [email, setEmail] = useState(instructor ? instructor.email : "");

  useEffect(() => {
    if (instructor) {
      setName(instructor.name);
      setEmail(instructor.email);
    }
  }, [instructor]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (instructor) {
      // Update
      api.put(`instructors/${instructor.id}/`, { name, email })
        .then(res => onAdded && onAdded())
        .catch(err => console.error(err));
    } else {
      // Create
      api.post("instructors/", { name, email })
        .then(res => {
          setName("");
          setEmail("");
          onAdded && onAdded();
        })
        .catch(err => console.error(err));
    }
  };

  return (
    <div className="bg-white p-4 rounded-lg shadow-md mb-4 w-full max-w-md">
      <h2 className="text-xl font-bold mb-3 text-gray-800">
        {instructor ? "Edit Instructor" : "Add Instructor"}
      </h2>
      <form className="flex flex-col gap-3" onSubmit={handleSubmit}>
        <input
          className="border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
          placeholder="Name"
          value={name}
          onChange={e => setName(e.target.value)}
          required
        />
        <input
          className="border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
          placeholder="Email"
          type="email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          required
        />
        <button
          className="bg-blue-500 text-white p-2 rounded hover:bg-blue-600 transition"
          type="submit"
        >
          {instructor ? "Update" : "Add"}
        </button>
      </form>
    </div>
  );
}

export default InstructorForm;
