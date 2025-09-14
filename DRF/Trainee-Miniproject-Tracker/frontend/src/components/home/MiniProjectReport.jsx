import { useEffect, useState } from "react";
import api from "../../api/api";
import toast from "react-hot-toast";

export default function MiniProjectReport() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchReport = async () => {
      setLoading(true);
      try {
        const res = await api.get("/projects/reports/mini-projects/");
        setProjects(res.data);
      } catch (err) {
        console.error(err);
        toast.error("Failed to fetch report");
      } finally {
        setLoading(false);
      }
    };

    fetchReport();
  }, []);

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6">Mini Project Completion Report</h1>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <table className="min-w-full border">
          <thead>
            <tr className="bg-gray-200">
              <th className="border px-4 py-2">Title</th>
              <th className="border px-4 py-2">Trainee</th>
              <th className="border px-4 py-2">Status</th>
              <th className="border px-4 py-2">Progress</th>
              <th className="border px-4 py-2">Due Date</th>
              <th className="border px-4 py-2">Completed</th>
            </tr>
          </thead>
          <tbody>
            {projects.map((p) => (
              <tr key={p.id} className="text-center">
                <td className="border px-4 py-2">{p.title}</td>
                <td className="border px-4 py-2">{p.assigned_to}</td>
                <td className="border px-4 py-2">{p.status}</td>
                <td className="border px-4 py-2">{p.progress}%</td>
                <td className="border px-4 py-2">{p.due_date || "N/A"}</td>
                <td className="border px-4 py-2">{p.completed ? "✅" : "❌"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
