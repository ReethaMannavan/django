import InstructorList from "./components/InstructorList";
import InstructorForm from "./components/InstructorForm";
import CourseList from "./components/CourseList";
import CourseForm from "./components/CourseForm";

function App() {
  return (
 <div className="min-h-screen bg-gray-100 p-6">
  <h1 className="text-3xl font-bold mb-6 text-center">
    Online Course Tracker
  </h1>

  <div className="flex flex-col md:flex-row gap-6 md:items-stretch">
    {/* Left Column */}
    <div className="md:w-1/2 flex flex-col gap-6 bg-gray-50 p-4 rounded-lg shadow-md h-full">
      <InstructorForm onAdded={() => window.location.reload()} />
      <InstructorList />
    </div>

    {/* Right Column */}
    <div className="md:w-1/2 flex flex-col gap-6 bg-gray-50 p-4 rounded-lg shadow-md h-full">
      <CourseForm onAdded={() => window.location.reload()} />
      <CourseList />
    </div>
  </div>
</div>

  );
}

export default App;
