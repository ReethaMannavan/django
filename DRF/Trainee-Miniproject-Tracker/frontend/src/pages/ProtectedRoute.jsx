import { Navigate } from "react-router-dom";

const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem("access");

  if (!token) {
    // Not logged in, redirect to login
    return <Navigate to="/login" replace />;
  }

  // Logged in, show the page
  return children;
};

export default ProtectedRoute;
