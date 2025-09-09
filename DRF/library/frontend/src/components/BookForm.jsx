import { useState, useEffect } from "react";
import api from "../api";

function BookForm({ onAdded, book }) {
  const [title, setTitle] = useState(book ? book.title : "");
  const [publishedYear, setPublishedYear] = useState(book ? book.published_year : "");
  const [authorId, setAuthorId] = useState(book ? book.author.id : "");
  const [authors, setAuthors] = useState([]);

  useEffect(() => {
    api.get("authors/").then(res => setAuthors(res.data));
  }, []);

  useEffect(() => {
    if (book) {
      setTitle(book.title);
      setPublishedYear(book.published_year);
      setAuthorId(book.author.id);
    }
  }, [book]);

  const handleSubmit = (e) => {
    e.preventDefault();
    const payload = { title, published_year: publishedYear, author_id: authorId };

    if (book) {
      api.put(`books/${book.id}/`, payload)
        .then(() => onAdded && onAdded())
        .catch(err => console.error(err));
    } else {
      api.post("books/", payload)
        .then(() => {
          setTitle(""); setPublishedYear(""); setAuthorId("");
          onAdded && onAdded();
        })
        .catch(err => console.error(err));
    }
  };

  return (
    <div className="bg-white p-4 rounded-lg shadow mb-4">
      <h2 className="text-lg font-bold mb-2">{book ? "Edit Book" : "Add Book"}</h2>
      <form onSubmit={handleSubmit} className="flex flex-col gap-2">
        <input className="border p-2 rounded" placeholder="Title"
          value={title} onChange={e => setTitle(e.target.value)} required />
        <input className="border p-2 rounded" placeholder="Published Year"
          type="number" value={publishedYear} onChange={e => setPublishedYear(e.target.value)} required />
        <select className="border p-2 rounded" value={authorId}
          onChange={e => setAuthorId(e.target.value)} required>
          <option value="">Select Author</option>
          {authors.map(a => (
            <option key={a.id} value={a.id}>{a.name}</option>
          ))}
        </select>
        <button className="bg-green-500 text-white px-3 py-2 rounded hover:bg-green-600">
          {book ? "Update" : "Add"}
        </button>
      </form>
    </div>
  );
}
export default BookForm;
