/** @type {import('tailwindcss').Config} */
export default {
  content: [
      "./index.html",              // Vite entry point
    "./src/**/*.{js,jsx,ts,tsx}" // All React component files
  ],
  theme: {
    extend: { 
    
  fontFamily: {
        roboto: ["Roboto", "sans-serif"],
      },
},
  },
  plugins: [
  ],
}

