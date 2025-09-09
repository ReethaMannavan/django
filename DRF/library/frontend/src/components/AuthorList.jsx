import { useEffect, useState } from "react";
import api from "../api";
import AuthorForm from "./AuthorForm";

function AuthorList() {
  const [authors, setAuthors] = useState([]);
  const [editingAuthor, setEditingAuthor] = useState(null);

  const fetchAuthors = () => {
    api.get("authors/").then(res => setAuthors(res.data));
  };

  useEffect(() => { fetchAuthors(); }, []);

  const handleDelete = (id) => {
    if (window.confirm("Delete this author?")) {
      api.delete(`authors/${id}/`).then(() => fetchAuthors());
    }
  };

  const handleUpdated = () => {
    setEditingAuthor(null);
    fetchAuthors();
  };

  return (
    <div id="authors" className="bg-gray-50 p-4 rounded-lg shadow">
      <h2 className="text-xl font-bold mb-3">Authors</h2>

      {editingAuthor && (
        <AuthorForm author={editingAuthor} onAdded={handleUpdated} />
      )}

      <ul className="space-y-2">
        {authors.map(a => (
          <li key={a.id} className="bg-white p-3 rounded shadow-sm flex justify-between items-center">
            <span>{a.name} ({a.email})</span>
            <div className="space-x-2">
              <button className="bg-yellow-400 px-2 py-1 rounded text-white"
                onClick={() => setEditingAuthor(a)}>Edit</button>
              <button className="bg-red-500 px-2 py-1 rounded text-white"
                onClick={() => handleDelete(a.id)}>Delete</button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
export default AuthorList;
