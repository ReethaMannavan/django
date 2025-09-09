import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="bg-blue-600 text-white px-6 py-3 flex justify-between items-center shadow-md">
      <h1 className="text-xl font-bold">📚 Simple Library</h1>
      <div className="space-x-4">
        <Link to="/" className="hover:text-gray-200">Home</Link>
        <Link to="/authors" className="hover:text-gray-200">Authors</Link>
        <Link to="/books" className="hover:text-gray-200">Books</Link>
      </div>
    </nav>
  );
}

export default Navbar;
