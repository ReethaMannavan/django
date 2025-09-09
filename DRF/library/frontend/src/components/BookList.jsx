import { useEffect, useState } from "react";
import api from "../api";
import BookForm from "./BookForm";

function BookList() {
  const [books, setBooks] = useState([]);
  const [filter, setFilter] = useState("");
  const [editingBook, setEditingBook] = useState(null);

  const fetchBooks = (author = "") => {
    let url = "books/";
    if (author) url += `?author=${author}`;
    api.get(url).then(res => setBooks(res.data));
  };

  useEffect(() => { fetchBooks(); }, []);

  const handleDelete = (id) => {
    if (window.confirm("Delete this book?")) {
      api.delete(`books/${id}/`).then(() => fetchBooks());
    }
  };

  const handleUpdated = () => {
    setEditingBook(null);
    fetchBooks();
  };

  return (
    <div id="books" className="bg-gray-50 p-4 rounded-lg shadow">
      <h2 className="text-xl font-bold mb-3">Books</h2>

      <input className="border p-2 rounded mb-3 w-full"
        placeholder="Filter by author name"
        value={filter}
        onChange={(e) => { setFilter(e.target.value); fetchBooks(e.target.value); }} />

      {editingBook && (
        <BookForm book={editingBook} onAdded={handleUpdated} />
      )}

      <ul className="space-y-2">
        {books.map(b => (
          <li key={b.id} className="bg-white p-3 rounded shadow-sm flex justify-between items-center">
            <span>
              <strong>{b.title}</strong> ({b.published_year}) - {b.author.name}
              <span className="text-sm text-gray-500 ml-2">Age: {b.book_age} yrs</span>
            </span>
            <div className="space-x-2">
              <button className="bg-yellow-400 px-2 py-1 rounded text-white"
                onClick={() => setEditingBook(b)}>Edit</button>
              <button className="bg-red-500 px-2 py-1 rounded text-white"
                onClick={() => handleDelete(b.id)}>Delete</button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
export default BookList;
