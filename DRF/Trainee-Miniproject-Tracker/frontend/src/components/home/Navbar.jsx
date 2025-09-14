// import { Link, useNavigate } from "react-router-dom";

// export default function Navbar() {
//   const navigate = useNavigate();
//   const role = localStorage.getItem("role");
//   const username = localStorage.getItem("username");

//   const handleLogout = () => {
//     localStorage.clear();
//     navigate("/login");
//   };

//   return (
//     <nav className="bg-[#07435C] text-white p-4 flex justify-between items-center shadow-md">
//       <Link to="/" className="text-xl font-bold hover:text-gray-300 transition">
//         Trainee Tracker
//       </Link>
//       <div className="flex items-center space-x-4">
//         {username && <span className="hidden sm:inline">Hello, {username} ({role})</span>}
//         {username ? (
//           <button
//             onClick={handleLogout}
//             className="bg-white text-[#07435C] px-3 py-1 rounded-full font-semibold hover:bg-gray-200 transition"
//           >
//             Logout
//           </button>
//         ) : (
//           <>
//             <Link to="/login" className="hover:text-gray-200 transition">
//               Login
//             </Link>
//             <Link to="/register" className="hover:text-gray-200 transition">
//               Register
//             </Link>
//           </>
//         )}
//       </div>
//     </nav>
//   );
// }



import { Link, useNavigate } from "react-router-dom";

export default function Navbar() {
  const navigate = useNavigate();
  const role = localStorage.getItem("role");
  const username = localStorage.getItem("username");
  const token = localStorage.getItem("access");

  const handleLogout = () => {
    localStorage.clear();
    navigate("/login");
  };

  return (
    <nav className="bg-[#07435C] text-white p-4 flex justify-between items-center shadow-md">
      <Link
        to={token ? "/dashboard" : "/"}
        className="text-xl font-bold hover:text-gray-300 transition"
      >
        Trainee Tracker
      </Link>
      <div className="flex items-center space-x-4">
        {username && <span className="hidden sm:inline">Hello, {username} ({role})</span>}
        {username ? (
          <button
            onClick={handleLogout}
            className="bg-white text-[#07435C] px-3 py-1 rounded-full font-semibold hover:bg-gray-200 transition"
          >
            Logout
          </button>
        ) : (
          <>
            <Link to="/login" className="hover:text-gray-200 transition">Login</Link>
            <Link to="/register" className="hover:text-gray-200 transition">Register</Link>
          </>
        )}
      </div>
    </nav>
  );
}
