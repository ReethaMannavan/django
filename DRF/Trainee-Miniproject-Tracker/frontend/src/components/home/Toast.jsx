export default function Toast({ message, show }) {
  return (
    show && (
      <div className="fixed top-5 right-5 bg-blue-500 text-white px-4 py-2 rounded-lg shadow-lg animate-bounce z-50">
        {message}
      </div>
    )
  );
}
