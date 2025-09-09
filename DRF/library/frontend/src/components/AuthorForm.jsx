import { useState, useEffect } from "react";
import api from "../api";

function AuthorForm({ onAdded, author }) {
  const [name, setName] = useState(author ? author.name : "");
  const [email, setEmail] = useState(author ? author.email : "");

  useEffect(() => {
    if (author) {
      setName(author.name);
      setEmail(author.email);
    }
  }, [author]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (author) {
      // Update
      api.put(`authors/${author.id}/`, { name, email })
        .then(() => onAdded && onAdded())
        .catch(err => console.error(err));
    } else {
      // Create
      api.post("authors/", { name, email })
        .then(() => {
          setName(""); setEmail("");
          onAdded && onAdded();
        })
        .catch(err => console.error(err));
    }
  };

  return (
    <div className="bg-white p-4 rounded-lg shadow mb-4">
      <h2 className="text-lg font-bold mb-2">{author ? "Edit Author" : "Add Author"}</h2>
      <form onSubmit={handleSubmit} className="flex flex-col gap-2">
        <input className="border p-2 rounded" placeholder="Name"
          value={name} onChange={e => setName(e.target.value)} required />
        <input className="border p-2 rounded" placeholder="Email"
          type="email" value={email} onChange={e => setEmail(e.target.value)} required />
        <button className="bg-blue-500 text-white px-3 py-2 rounded hover:bg-blue-600">
          {author ? "Update" : "Add"}
        </button>
      </form>
    </div>
  );
}
export default AuthorForm;
