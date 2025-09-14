import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { Toaster } from "react-hot-toast";

import "./App.css";
import "./index.css";
import ProtectedRoute from "./pages/ProtectedRoute"; 

import HomePage from "./pages/HomePage";
import Login from "./components/login/Login";
import Register from "./components/login/Register";
import Dashboard from "./components/home/Dashboard";

function App() {
  const token = localStorage.getItem("access"); // check if user is logged in

  return (
    <Router>
      <div className="min-h-screen font-roboto bg-gray-100">
        <Toaster position="top-center" reverseOrder={false} />
        <Routes>
          {/* Home redirects logged-in users to dashboard */}
          <Route path="/" element={token ? <Navigate to="/dashboard" /> : <HomePage />} />
          
          {/* Login/Register redirects logged-in users to dashboard */}
          <Route path="/login" element={token ? <Navigate to="/dashboard" /> : <Login />} />
          <Route path="/register" element={token ? <Navigate to="/dashboard" /> : <Register />} />

          {/* Protected dashboard route */}
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
