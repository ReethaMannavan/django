import { useEffect, useState } from "react";
import api from "../api/api";
import Navbar from "../components/home/Navbar";
import { Link } from "react-router-dom";

const HomePage = () => {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState("");
  const [priorityFilter, setPriorityFilter] = useState("");
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const [pageSize] = useState(6);

  const token = localStorage.getItem("access");
  const role = localStorage.getItem("role");
  const user_id = parseInt(localStorage.getItem("user_id"));
  const isLoggedIn = !!token;

  useEffect(() => {
    const fetchProjects = async () => {
      setLoading(true);
      try {
        const endpoint = isLoggedIn ? "/projects/" : "/projects/public-mini-projects/";
        const res = await api.get(endpoint);
        let data = Array.isArray(res.data) ? res.data : res.data.results || [];

        if (role === "trainee") {
          data = data.filter((p) => p.assigned_to?.id === user_id);
        }
        setProjects(data);
      } catch (err) {
        console.error("Failed to fetch projects", err);
        setProjects([]);
      } finally {
        setLoading(false);
      }
    };
    fetchProjects();
  }, [isLoggedIn, role, user_id]);

  const filteredProjects = projects
    .filter((p) => (statusFilter ? p.status === statusFilter : true))
    .filter((p) => (priorityFilter ? p.priority === priorityFilter : true))
    .filter((p) =>
      search
        ? p.title.toLowerCase().includes(search.toLowerCase()) ||
          p.description.toLowerCase().includes(search.toLowerCase())
        : true
    );

  const totalPages = Math.max(Math.ceil(filteredProjects.length / pageSize), 1);
  const displayedProjects = filteredProjects.slice((page - 1) * pageSize, page * pageSize);

  const getStatusColor = (status) => {
    switch (status) {
      case "assigned":
        return "text-blue-500";
      case "inprogress":
        return "text-yellow-500";
      case "completed":
        return "text-green-500";
      default:
        return "text-gray-500";
    }
  };

  return (
    <div className="flex flex-col min-h-screen bg-gray-100">
      <Navbar />

      <main className="flex-grow p-6">
        <h1 className="text-3xl font-bold mb-6 text-[#07435C] text-center">
          Trainee Mini Projects
        </h1>

        {!isLoggedIn && (
          <div className="text-center mb-6 p-4 bg-yellow-100 rounded-lg">
            <p className="text-gray-800">
              Please{" "}
              <Link to="/register" className="text-blue-500 font-semibold underline">Register</Link>{" "}
              or{" "}
              <Link to="/login" className="text-blue-500 font-semibold underline">Login</Link>{" "}
              to view your full dashboard and track projects.
            </p>
          </div>
        )}

        {/* Filters */}
        <div className="flex flex-col sm:flex-row justify-between items-center gap-4 mb-6">
          <input
            type="text"
            placeholder="Search projects..."
            value={search}
            onChange={(e) => { setSearch(e.target.value); setPage(1); }}
            className="px-4 py-2 rounded-full border focus:outline-none focus:ring-2 focus:ring-[#07435C] w-full sm:w-1/3"
          />
          <select
            value={statusFilter}
            onChange={(e) => { setStatusFilter(e.target.value); setPage(1); }}
            className="px-4 py-2 rounded-full border focus:outline-none focus:ring-2 focus:ring-[#07435C]"
          >
            <option value="">All Status</option>
            <option value="assigned">Assigned</option>
            <option value="inprogress">In Progress</option>
            <option value="completed">Completed</option>
          </select>
          <select
            value={priorityFilter}
            onChange={(e) => { setPriorityFilter(e.target.value); setPage(1); }}
            className="px-4 py-2 rounded-full border focus:outline-none focus:ring-2 focus:ring-[#07435C]"
          >
            <option value="">All Priority</option>
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </div>

        {/* Loading / Empty State */}
        {loading ? (
          <div className="text-center text-gray-500">Loading projects...</div>
        ) : displayedProjects.length === 0 ? (
          <div className="text-center text-gray-500">
            {isLoggedIn ? "No projects assigned to you yet." : "No public projects found."}
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {displayedProjects.map((project) => (
              <div key={project.id} className="bg-white rounded-2xl p-4 shadow-md hover:shadow-xl transition transform hover:-translate-y-1 hover:scale-105">
                <h2 className="text-xl font-semibold mb-2">{project.title}</h2>
                <p className="text-gray-600 mb-2 text-lg">{project.description}</p>
                <p className="text-md text-gray-500">
                  Assigned To: {project.assigned_to?.username || "Unassigned"}
                </p>
                <p className="text-md text-gray-500">
                  Assigned By: {project.assigned_by?.username || "N/A"}
                </p>
                <p className={`text-md font-semibold ${getStatusColor(project.status)}`}>
                  Status: {project.status === "assigned" ? "Assigned" : project.status === "inprogress" ? "In Progress" : "Completed"}
                </p>
                <p className="text-md text-gray-500">
                  Priority:{" "}
                  <span className={`font-semibold ${project.priority === "high" ? "text-red-500" : project.priority === "medium" ? "text-yellow-500" : "text-green-500"}`}>
                    {project.priority || "low"}
                  </span>
                </p>
              </div>
            ))}
          </div>
        )}

        {/* Pagination */}
        <div className="flex justify-center mt-6 gap-2 flex-wrap items-center">
          <button onClick={() => setPage((prev) => Math.max(prev - 1, 1))} disabled={page === 1} className="px-4 py-2 rounded-full border bg-white text-gray-700 hover:bg-[#07435C] hover:text-white disabled:bg-gray-200 disabled:text-gray-400">Prev</button>
          {Array.from({ length: totalPages }, (_, i) => (
            <button key={i + 1} onClick={() => setPage(i + 1)} className={`px-4 py-2 rounded-full border ${page === i + 1 ? "bg-[#07435C] text-white" : "bg-white text-gray-700 hover:bg-[#07435C] hover:text-white"}`}>{i + 1}</button>
          ))}
          <button onClick={() => setPage((prev) => Math.min(prev + 1, totalPages))} disabled={page === totalPages} className="px-4 py-2 rounded-full border bg-white text-gray-700 hover:bg-[#07435C] hover:text-white disabled:bg-gray-200 disabled:text-gray-400">Next</button>
        </div>
      </main>
    </div>
  );
};

export default HomePage;
