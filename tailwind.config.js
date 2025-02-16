/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/*.html",
  ],
  theme: {
    extend: {
      colors: {
        web_green: "#96bb96",
        text_light: "#f9f8f1",
        text_dark: "#2e2e27",
        dark_bg: "#061f13",
      },
      container: {
        center: true,
        padding: {
          DEFAULT: '1rem',
          sm: '2rem',
          md: '3rem',
          lg: '4rem',
          xl: '5rem',
        },
        screens: {
          sm: '640px',
          md: '768px',
          lg: '1024px',
          xl: '1280px',
        }
      },
      fontFamily: {
        'calisto': ['calisto', 'cursive'],
        'poppins': ['poppins', 'sans-serif'],
      }
    }
  },
  plugins: [],
}

