import { useEffect, useState } from "react";
import api from "../api";

function HomePage() {
  const [books, setBooks] = useState([]);

  useEffect(() => {
    api.get("books/").then(res => setBooks(res.data));
  }, []);

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Library Books</h2>
      <ul className="space-y-2">
        {books.map(book => (
          <li key={book.id} className="bg-white p-3 rounded shadow hover:shadow-md transition">
            <span className="font-semibold">{book.author.name}</span> - {book.title} ({book.published_year})
          </li>
        ))}
      </ul>
    </div>
  );
}

export default HomePage;
