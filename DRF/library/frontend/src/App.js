import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import AuthorList from "./components/AuthorList";
import AuthorForm from "./components/AuthorForm";
import BookList from "./components/BookList";
import BookForm from "./components/BookForm";
import HomePage from "./components/HomePage";

function App() {

  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        <Navbar />

        <div className="p-6">
          <Routes>

            <Route path="/" element={<HomePage />} />
            <Route path="/" element={<h2 className="text-2xl text-center">Welcome to Library 📖</h2>} />

            <Route
              path="/authors"
              element={
                <div className="flex flex-col gap-6">
                  <AuthorForm />
                  <AuthorList />
                </div>
              }
            />

            <Route
              path="/books"
              element={
                <div className="flex flex-col gap-6">
                  <BookForm />
                  <BookList />
                </div>
              }
            />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
