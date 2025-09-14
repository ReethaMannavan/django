import { useState } from "react";
import { useNavigate, useLocation, Link } from "react-router-dom";
import api from "../../api/api";
import Navbar from "../home/Navbar";

export default function Login() {
  const navigate = useNavigate();
  const location = useLocation();
  const [form, setForm] = useState({ username: "", password: "" });
  const [fieldError, setFieldError] = useState({});
  const [toast, setToast] = useState("");
  const [showToast, setShowToast] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const redirectPath = location.state?.from || "/dashboard";

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    setFieldError({ ...fieldError, [e.target.name]: "" });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (submitting) return;
    setSubmitting(true);
    setFieldError({});
    
    if (!form.username || !form.password) {
      setFieldError({
        username: !form.username ? "Username required" : "",
        password: !form.password ? "Password required" : "",
      });
      setSubmitting(false);
      return;
    }

    try {
      // 1️⃣ Login API
      const res = await api.post("/auth/token/", {
        username: form.username,
        password: form.password,
      });

      localStorage.setItem("access", res.data.access);
      localStorage.setItem("refresh", res.data.refresh);

      // 2️⃣ Get profile (role)
      const profileRes = await api.get("/projects/auth/profile/", {
        headers: { Authorization: `Bearer ${res.data.access}` },
      });

      localStorage.setItem("role", profileRes.data.role);
      localStorage.setItem("username", profileRes.data.username);

      // 3️⃣ Redirect
      navigate(redirectPath);
    } catch (err) {
      setToast("Invalid username or password");
      setShowToast(true);
      setTimeout(() => setShowToast(false), 3000);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <>
      <Navbar />
      {showToast && (
        <div className="fixed top-5 right-5 bg-red-500 text-white px-4 py-2 rounded-lg shadow-lg z-50">
          {toast}
        </div>
      )}
      <div className="flex min-h-screen items-center justify-center bg-gray-100 p-4">
        <div className="w-full max-w-md p-8 bg-white rounded-2xl shadow-lg animate-fadeIn">
          <h2 className="text-3xl font-bold mb-6 text-center text-[#07435C]">Log in</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-md text-[#07435C] mb-1">Username</label>
              <input
                type="text"
                name="username"
                value={form.username}
                onChange={handleChange}
                className="w-full rounded-full border px-4 py-2 focus:outline-none focus:ring-2 focus:ring-[#07435C]"
              />
              {fieldError.username && <p className="text-red-500 text-sm mt-1">{fieldError.username}</p>}
            </div>

            <div>
              <label className="block text-md text-[#07435C] mb-1">Password</label>
              <input
                type="password"
                name="password"
                value={form.password}
                onChange={handleChange}
                className="w-full rounded-full border px-4 py-2 focus:outline-none focus:ring-2 focus:ring-[#07435C]"
              />
              {fieldError.password && <p className="text-red-500 text-sm mt-1">{fieldError.password}</p>}
            </div>

            <button
              type="submit"
              disabled={submitting}
              className={`w-full rounded-full bg-[#07435C] text-white py-2 font-semibold hover:bg-[#052934] transition ${
                submitting ? "opacity-50 cursor-not-allowed" : ""
              }`}
            >
              {submitting ? "Logging in..." : "Log in"}
            </button>
          </form>
          <p className="mt-4 text-center text-sm">
            New User?{" "}
            <Link to="/register" className="text-[#07435C] font-semibold hover:underline">
              Register Here
            </Link>
          </p>
        </div>
      </div>
    </>
  );
}
