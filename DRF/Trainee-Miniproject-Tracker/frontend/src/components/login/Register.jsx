import { useState } from "react";
import { useNavigate, useLocation, Link } from "react-router-dom";
import api from "../../api/api";
import Navbar from "../home/Navbar";

export default function Register() {
  const navigate = useNavigate();
  const location = useLocation();

  const [form, setForm] = useState({
    email: "",
    username: location.state?.username || "",
    password: "",
    password2: "",
    role: "trainee",
  });
  const [fieldError, setFieldError] = useState({});
  const [toast, setToast] = useState("");
  const [showToast, setShowToast] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const redirectPath = location.state?.from || "/";

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    setFieldError({ ...fieldError, [e.target.name]: "" });
  };

  const validate = () => {
    let errors = {};
    if (!form.email) errors.email = "Email is required";
    if (!form.username) errors.username = "Username is required";
    if (form.password.length < 6) errors.password = "Password must be at least 6 characters";
    if (form.password !== form.password2) errors.password2 = "Passwords do not match";
    return errors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (submitting) return; // prevent double click
    setSubmitting(true);
    setFieldError({});

    const errors = validate();
    if (Object.keys(errors).length > 0) {
      setFieldError(errors);
      setSubmitting(false);
      return;
    }

    try {
      // 1️⃣ Register user
      await api.post("/projects/auth/register/", form);

      // 2️⃣ Login user immediately after successful registration
      const loginRes = await api.post("/auth/token/", {
        username: form.username,
        password: form.password,
      });

      localStorage.setItem("access", loginRes.data.access);
      localStorage.setItem("refresh", loginRes.data.refresh);

      // 3️⃣ Fetch user profile to get role
      const profileRes = await api.get("/projects/auth/profile/", {
        headers: { Authorization: `Bearer ${loginRes.data.access}` },
      });

      localStorage.setItem("role", profileRes.data.role);
      localStorage.setItem("username", form.username);

      setToast("Registration successful! Logged in.");
      setShowToast(true);
      setTimeout(() => setShowToast(false), 3000);

      // 4️⃣ Redirect to dashboard/homepage
      navigate(redirectPath);

    } catch (err) {
      if (err.response?.data?.username) setFieldError({ username: err.response.data.username[0] });
      else if (err.response?.data?.email) setFieldError({ email: err.response.data.email[0] });
      else {
        setToast("Registration failed. Try again!");
        setShowToast(true);
        setTimeout(() => setShowToast(false), 3000);
      }
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <>
      <Navbar />
      {showToast && (
        <div className="fixed top-5 right-5 bg-blue-500 text-white px-4 py-2 rounded-lg shadow-lg z-50 animate-bounce">
          {toast}
        </div>
      )}
      <div className="flex min-h-screen items-center justify-center bg-gray-100 p-4">
        <div className="w-full max-w-md p-8 bg-white rounded-2xl shadow-lg animate-fadeIn">
          <h2 className="text-3xl font-bold mb-6 text-center text-[#07435C]">Register</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-md text-[#07435C] mb-1">Email</label>
              <input
                type="email"
                name="email"
                value={form.email}
                onChange={handleChange}
                className="w-full rounded-full border px-4 py-2 focus:outline-none focus:ring-2 focus:ring-[#07435C]"
              />
              {fieldError.email && <p className="text-red-500 text-sm mt-1">{fieldError.email}</p>}
            </div>

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

            <div>
              <label className="block text-md text-[#07435C] mb-1">Confirm Password</label>
              <input
                type="password"
                name="password2"
                value={form.password2}
                onChange={handleChange}
                className="w-full rounded-full border px-4 py-2 focus:outline-none focus:ring-2 focus:ring-[#07435C]"
              />
              {fieldError.password2 && <p className="text-red-500 text-sm mt-1">{fieldError.password2}</p>}
            </div>

            <div>
              <label className="block text-md text-[#07435C] mb-1">Role</label>
              <select
                name="role"
                value={form.role}
                onChange={handleChange}
                className="w-full rounded-full border px-4 py-2 focus:outline-none focus:ring-2 focus:ring-[#07435C]"
              >
                <option value="trainee">Trainee</option>
                <option value="trainer">Trainer</option>
              </select>
            </div>

            <button
              type="submit"
              disabled={submitting}
              className={`w-full rounded-full bg-[#07435C] text-white py-2 font-semibold hover:bg-[#052934] transition ${submitting ? "opacity-50 cursor-not-allowed" : ""}`}
            >
              {submitting ? "Registering..." : "Register"}
            </button>
          </form>
          <p className="mt-4 text-center text-sm">
            Already have an account?{" "}
            <Link to="/login" className="text-[#07435C] font-semibold hover:underline">
              Log in here
            </Link>
          </p>
        </div>
      </div>
    </>
  );
}
