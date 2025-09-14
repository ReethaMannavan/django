
// import { useEffect, useState } from "react";
// import api from "../../api/api";
// import Navbar from "../../components/home/Navbar";
// import toast from "react-hot-toast";

// export default function DashboardNew() {
//   const [projects, setProjects] = useState([]);
//   const [users, setUsers] = useState([]);
//   const [loading, setLoading] = useState(true);
//   const [modalOpen, setModalOpen] = useState(false);
//   const [currentProject, setCurrentProject] = useState(null);
//   const [form, setForm] = useState({
//     title: "",
//     description: "",
//     assigned_to_id: "",
//     priority: "medium",
//     status: "assigned",
//     due_date: "",
//   });

//   const role = localStorage.getItem("role");
//   const username = localStorage.getItem("username");

//   // Filters
//   const [statusFilter, setStatusFilter] = useState("");
//   const [priorityFilter, setPriorityFilter] = useState("");

//   // Pagination
//   const [page, setPage] = useState(1);
//   const [totalPages, setTotalPages] = useState(1);

//   useEffect(() => {
//     const initDashboard = async () => {
//       await fetchProjects();
//       if (role === "trainer") await fetchUsers();
//     };
//     initDashboard();
//     // eslint-disable-next-line react-hooks/exhaustive-deps
//   }, [statusFilter, priorityFilter, page]);

//   const fetchProjects = async () => {
//     setLoading(true);
//     try {
//       const res = await api.get("/projects/mini-projects/", {
//         params: { status: statusFilter, priority: priorityFilter, page },
//       });

//       let data = res.data.results;

//       // Trainee sees only their assigned projects
//       if (role === "trainee") {
//         data = data.filter((p) => p.assigned_to?.username === username);
//       }

//       // Trainer sees only projects they created
//       if (role === "trainer") {
//         data = data.filter((p) => p.assigned_by?.username === username);
//       }

//       setProjects(data);
//       setTotalPages(Math.ceil(res.data.count / 6) || 1);
//     } catch (err) {
//       console.error("❌ Fetch projects error:", err.response?.data || err);
//       toast.error("Failed to fetch projects");
//     } finally {
//       setLoading(false);
//     }
//   };

//   const fetchUsers = async () => {
//     try {
//       const res = await api.get("/projects/auth/trainees/");
//       setUsers(res.data);
//     } catch (err) {
//       console.error("❌ Fetch users error:", err.response?.data || err);
//       toast.error("Failed to fetch users");
//     }
//   };

//   const handleChange = (e) =>
//     setForm({ ...form, [e.target.name]: e.target.value });

//   const openModal = (project = null) => {
//     if (project) {
//       setCurrentProject(project);
//       setForm({
//         title: project.title,
//         description: project.description,
//         assigned_to_id: project.assigned_to?.id || "",
//         priority: project.priority,
//         status: project.status,
//         due_date: project.due_date || "",
//       });
//     } else {
//       setCurrentProject(null);
//       setForm({
//         title: "",
//         description: "",
//         assigned_to_id: "",
//         priority: "medium",
//         status: "assigned",
//         due_date: "",
//       });
//     }
//     setModalOpen(true);
//   };

//  const handleSubmit = async (e) => {
//   e.preventDefault();
//   try {
//     let payload = {};

//     if (role === "trainee") {
//       // Trainee only updates status
//       payload.status = form.status;
//       await api.patch(`/projects/mini-projects/${currentProject.id}/`, payload);
//     } else {
//       // Trainer updates everything
//       payload = {
//         title: form.title,
//         description: form.description,
//         priority: form.priority,
//         status: form.status,
//         due_date: form.due_date || null,
//       };
//       if (form.assigned_to_id) payload.assigned_to_id = form.assigned_to_id;
//       if (currentProject) {
//         await api.put(`/projects/mini-projects/${currentProject.id}/`, payload);
//       } else {
//         await api.post("/projects/mini-projects/", payload);
//       }
//     }

//     toast.success("Project updated successfully");
//     setModalOpen(false);
//     fetchProjects();
//   } catch (err) {
//     console.error("❌ Project save error:", err.response?.data || err);
//     toast.error("Action failed");
//   }
// };

//   const handleDelete = async (id) => {
//     if (!window.confirm("Are you sure you want to delete this project?")) return;
//     try {
//       await api.delete(`/projects/mini-projects/${id}/`);
//       toast.success("Project deleted successfully");
//       setProjects(projects.filter((p) => p.id !== id));
//     } catch (err) {
//       console.error("❌ Delete error:", err.response?.data || err);
//       toast.error("Delete failed");
//     }
//   };

//   return (
//     <div className="min-h-screen bg-gray-100">
//       <Navbar />

//       <div className="container mx-auto p-4">
//         <h1 className="text-3xl font-bold text-[#07435C] mb-6">Dashboard</h1>

//         {/* Filters and Create */}
//         <div className="flex flex-wrap gap-4 mb-4">
//           <select
//             value={statusFilter}
//             onChange={(e) => setStatusFilter(e.target.value)}
//             className="px-3 py-2 rounded-full border"
//           >
//             <option value="">All Status</option>
//             <option value="assigned">Assigned</option>
//             <option value="inprogress">In Progress</option>
//             <option value="completed">Completed</option>
//           </select>

//           <select
//             value={priorityFilter}
//             onChange={(e) => setPriorityFilter(e.target.value)}
//             className="px-3 py-2 rounded-full border"
//           >
//             <option value="">All Priority</option>
//             <option value="low">Low</option>
//             <option value="medium">Medium</option>
//             <option value="high">High</option>
//           </select>

//           {role === "trainer" && (
//             <button
//               onClick={() => openModal()}
//               className="ml-auto px-4 py-2 bg-[#07435C] text-white rounded-full"
//             >
//               + Create Project
//             </button>
//           )}
//         </div>

//         {/* Projects */}
//         {loading ? (
//           <div className="text-center text-gray-500">Loading...</div>
//         ) : projects.length === 0 ? (
//           <div className="text-center text-gray-500">
//             No projects to display.
//           </div>
//         ) : (
//           <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
//             {projects.map((p) => (
//               <div key={p.id} className="bg-white p-4 rounded-2xl shadow-md">
//                 <h2 className="text-xl font-semibold">{p.title}</h2>
//                 <p>{p.description}</p>
//                 <p>Assigned To: {p.assigned_to?.username || "N/A"}</p>
//                 <p>Assigned By: {p.assigned_by?.username || "N/A"}</p>
//                 <p>Status: {p.status}</p>
//                 <p>Priority: {p.priority}</p>
//                 <p>Due: {p.due_date || "N/A"}</p>

//                 <div className="flex gap-2 mt-2">
//                   <button
//                     onClick={() => openModal(p)}
//                     className="px-3 py-1 bg-yellow-500 text-white rounded-full"
//                   >
//                     Update
//                   </button>
//                   {role === "trainer" && (
//                     <button
//                       onClick={() => handleDelete(p.id)}
//                       className="px-3 py-1 bg-red-500 text-white rounded-full"
//                     >
//                       Delete
//                     </button>
//                   )}
//                 </div>
//               </div>
//             ))}
//           </div>
//         )}
//       </div>

//       {/* Modal */}
//       {modalOpen && (
//         <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
//           <div className="bg-white p-6 rounded-2xl w-11/12 max-w-lg">
//             <h2 className="text-xl font-semibold mb-4">
//               {currentProject ? "Update Project" : "Create Project"}
//             </h2>
//             <form onSubmit={handleSubmit} className="flex flex-col gap-3">
//               {/* Trainer fields */}
//               {role === "trainer" && (
//                 <>
//                   <input
//                     name="title"
//                     value={form.title}
//                     onChange={handleChange}
//                     placeholder="Title"
//                     className="px-3 py-2 rounded-full border"
//                     required
//                   />
//                   <textarea
//                     name="description"
//                     value={form.description}
//                     onChange={handleChange}
//                     placeholder="Description"
//                     className="px-3 py-2 rounded-2xl border"
//                   />
//                   <select
//                     name="assigned_to_id"
//                     value={form.assigned_to_id}
//                     onChange={handleChange}
//                     className="px-3 py-2 rounded-full border"
//                   >
//                     <option value="">Select Trainee</option>
//                     {users.map((u) => (
//                       <option key={u.id} value={u.id}>
//                         {u.username}
//                       </option>
//                     ))}
//                   </select>
//                   <select
//                     name="priority"
//                     value={form.priority}
//                     onChange={handleChange}
//                     className="px-3 py-2 rounded-full border"
//                   >
//                     <option value="low">Low</option>
//                     <option value="medium">Medium</option>
//                     <option value="high">High</option>
//                   </select>
//                 </>
//               )}

//               {/* Status available for both roles */}
//               <select
//                 name="status"
//                 value={form.status}
//                 onChange={handleChange}
//                 className="px-3 py-2 rounded-full border"
//               >
//                 <option value="assigned">Assigned</option>
//                 <option value="inprogress">In Progress</option>
//                 <option value="completed">Completed</option>
//               </select>

//               <input
//                 type="date"
//                 name="due_date"
//                 value={form.due_date}
//                 onChange={handleChange}
//                 className="px-3 py-2 rounded-full border"
//                 disabled={role === "trainee"} // trainee cannot change due date
//               />

//               <div className="flex justify-end gap-2 mt-2">
//                 <button
//                   type="button"
//                   onClick={() => setModalOpen(false)}
//                   className="px-4 py-2 bg-gray-300 rounded-full"
//                 >
//                   Cancel
//                 </button>
//                 <button
//                   type="submit"
//                   className="px-4 py-2 bg-[#07435C] text-white rounded-full"
//                 >
//                   {currentProject ? "Update" : "Create"}
//                 </button>
//               </div>
//             </form>
//           </div>
//         </div>
//       )}
//     </div>
//   );
// }



import { useEffect, useState } from "react";
import api from "../../api/api";
import Navbar from "../../components/home/Navbar";
import toast from "react-hot-toast";

export default function DashboardNew() {
  const [projects, setProjects] = useState([]);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [currentProject, setCurrentProject] = useState(null);
  const [form, setForm] = useState({
    title: "",
    description: "",
    assigned_to_id: "",
    priority: "medium",
    status: "assigned",
    due_date: "",
  });

  const role = localStorage.getItem("role");
  const username = localStorage.getItem("username");

  // Filters
  const [statusFilter, setStatusFilter] = useState("");
  const [priorityFilter, setPriorityFilter] = useState("");

  // Pagination
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    const initDashboard = async () => {
      await fetchProjects();
      if (role === "trainer") await fetchUsers();
    };
    initDashboard();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [statusFilter, priorityFilter, page]);

  const fetchProjects = async () => {
    setLoading(true);
    try {
      const res = await api.get("/projects/mini-projects/", {
        params: { status: statusFilter, priority: priorityFilter, page },
      });

      let data = res.data.results;

      // Trainee sees only their assigned projects
      if (role === "trainee") {
        data = data.filter((p) => p.assigned_to?.username === username);
      }

      // Trainer sees only projects they created
      if (role === "trainer") {
        data = data.filter((p) => p.assigned_by?.username === username);
      }

      setProjects(data);
      setTotalPages(Math.ceil(res.data.count / 6) || 1);
    } catch (err) {
      console.error("❌ Fetch projects error:", err.response?.data || err);
      toast.error("Failed to fetch projects");
    } finally {
      setLoading(false);
    }
  };

  const fetchUsers = async () => {
    try {
      const res = await api.get("/projects/auth/trainees/");
      setUsers(res.data);
    } catch (err) {
      console.error("❌ Fetch users error:", err.response?.data || err);
      toast.error("Failed to fetch users");
    }
  };

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const openModal = (project = null) => {
    if (project) {
      setCurrentProject(project);
      setForm({
        title: project.title,
        description: project.description,
        assigned_to_id: project.assigned_to?.id || "",
        priority: project.priority,
        status: project.status,
        due_date: project.due_date || "",
      });
    } else {
      setCurrentProject(null);
      setForm({
        title: "",
        description: "",
        assigned_to_id: "",
        priority: "medium",
        status: "assigned",
        due_date: "",
      });
    }
    setModalOpen(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      let payload = {};

      if (role === "trainee") {
        // Trainee only updates status
        payload.status = form.status;
        await api.patch(`/projects/mini-projects/${currentProject.id}/`, payload);
      } else {
        // Trainer updates everything
        payload = {
          title: form.title,
          description: form.description,
          priority: form.priority,
          status: form.status,
          due_date: form.due_date || null,
        };
        if (form.assigned_to_id) payload.assigned_to_id = form.assigned_to_id;
        if (currentProject) {
          await api.put(`/projects/mini-projects/${currentProject.id}/`, payload);
        } else {
          await api.post("/projects/mini-projects/", payload);
        }
      }

      toast.success("Project updated successfully");
      setModalOpen(false);
      fetchProjects();
    } catch (err) {
      console.error("❌ Project save error:", err.response?.data || err);
      toast.error("Action failed");
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this project?")) return;
    try {
      await api.delete(`/projects/mini-projects/${id}/`);
      toast.success("Project deleted successfully");
      setProjects(projects.filter((p) => p.id !== id));
    } catch (err) {
      console.error("❌ Delete error:", err.response?.data || err);
      toast.error("Delete failed");
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar />

      <div className="container mx-auto p-4">
        <h1 className="text-3xl font-bold text-[#07435C] mb-6">Dashboard</h1>

        {/* Filters and Create */}
        <div className="flex flex-wrap gap-4 mb-4">
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="px-3 py-2 rounded-full border"
          >
            <option value="">All Status</option>
            <option value="assigned">Assigned</option>
            <option value="inprogress">In Progress</option>
            <option value="completed">Completed</option>
          </select>

          <select
            value={priorityFilter}
            onChange={(e) => setPriorityFilter(e.target.value)}
            className="px-3 py-2 rounded-full border"
          >
            <option value="">All Priority</option>
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>

          {role === "trainer" && (
            <button
              onClick={() => openModal()}
              className="ml-auto px-4 py-2 bg-[#07435C] text-white rounded-full"
            >
              + Create Project
            </button>
          )}
        </div>

        {/* Projects */}
        {loading ? (
          <div className="text-center text-gray-500">Loading...</div>
        ) : projects.length === 0 ? (
          <div className="text-center text-gray-500">
            No projects to display.
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {projects.map((p) => (
              <div key={p.id} className="bg-white p-4 rounded-2xl shadow-md">
                <h2 className="text-xl font-semibold">{p.title}</h2>
                <p>{p.description}</p>
                <p>Assigned To: {p.assigned_to?.username || "N/A"}</p>
                <p>Assigned By: {p.assigned_by?.username || "N/A"}</p>
                <p>Status: {p.status}</p>
                <p>Priority: {p.priority}</p>
                <p>Due: {p.due_date || "N/A"}</p>

                <div className="flex gap-2 mt-2">
                  <button
                    onClick={() => openModal(p)}
                    className="px-3 py-1 bg-yellow-500 text-white rounded-full"
                  >
                    Update
                  </button>
                  {role === "trainer" && (
                    <button
                      onClick={() => handleDelete(p.id)}
                      className="px-3 py-1 bg-red-500 text-white rounded-full"
                    >
                      Delete
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Trainer Report */}
        {role === "trainer" && projects.length > 0 && (
          <div className="mt-10">
            <h2 className="text-2xl font-semibold text-[#07435C] mb-4">
              Trainer Report: Project Completion
            </h2>
            <div className="overflow-x-auto bg-white rounded-2xl shadow-md p-4">
              <table className="min-w-full text-left border-collapse">
                <thead>
                  <tr className="border-b">
                    <th className="px-4 py-2">Project Title</th>
                    <th className="px-4 py-2">Assigned To</th>
                    <th className="px-4 py-2">Status</th>
                    <th className="px-4 py-2">Due Date</th>
                  </tr>
                </thead>
                <tbody>
                  {projects.map((p) => (
                    <tr key={p.id} className="border-b hover:bg-gray-50">
                      <td className="px-4 py-2">{p.title}</td>
                      <td className="px-4 py-2">{p.assigned_to?.username || "N/A"}</td>
                      <td className="px-4 py-2">
                        {p.status === "completed" ? (
                          <span className="text-green-600 font-semibold">Completed</span>
                        ) : (
                          <span className="text-red-600 font-semibold">{p.status}</span>
                        )}
                      </td>
                      <td className="px-4 py-2">{p.due_date || "N/A"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>

      {/* Modal */}
      {modalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-2xl w-11/12 max-w-lg">
            <h2 className="text-xl font-semibold mb-4">
              {currentProject ? "Update Project" : "Create Project"}
            </h2>
            <form onSubmit={handleSubmit} className="flex flex-col gap-3">
              {/* Trainer fields */}
              {role === "trainer" && (
                <>
                  <input
                    name="title"
                    value={form.title}
                    onChange={handleChange}
                    placeholder="Title"
                    className="px-3 py-2 rounded-full border"
                    required
                  />
                  <textarea
                    name="description"
                    value={form.description}
                    onChange={handleChange}
                    placeholder="Description"
                    className="px-3 py-2 rounded-2xl border"
                  />
                  <select
                    name="assigned_to_id"
                    value={form.assigned_to_id}
                    onChange={handleChange}
                    className="px-3 py-2 rounded-full border"
                  >
                    <option value="">Select Trainee</option>
                    {users.map((u) => (
                      <option key={u.id} value={u.id}>
                        {u.username}
                      </option>
                    ))}
                  </select>
                  <select
                    name="priority"
                    value={form.priority}
                    onChange={handleChange}
                    className="px-3 py-2 rounded-full border"
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                  </select>
                </>
              )}

              {/* Status available for both roles */}
              <select
                name="status"
                value={form.status}
                onChange={handleChange}
                className="px-3 py-2 rounded-full border"
              >
                <option value="assigned">Assigned</option>
                <option value="inprogress">In Progress</option>
                <option value="completed">Completed</option>
              </select>

              <input
                type="date"
                name="due_date"
                value={form.due_date}
                onChange={handleChange}
                className="px-3 py-2 rounded-full border"
                disabled={role === "trainee"} // trainee cannot change due date
              />

              <div className="flex justify-end gap-2 mt-2">
                <button
                  type="button"
                  onClick={() => setModalOpen(false)}
                  className="px-4 py-2 bg-gray-300 rounded-full"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-[#07435C] text-white rounded-full"
                >
                  {currentProject ? "Update" : "Create"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
