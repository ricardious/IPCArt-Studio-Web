/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.html", "./**/templates/**/*.html"],
  darkMode: "media",
  theme: {
    extend: {
      backgroundImage: {
        'pixel': "url('/static/images/bg-pixel.jpg')",
      },
      fontFamily: {
        title: ["Pixelify Sans", "sans-serif"],
      },
      spacing: {
        'calc-100-58': 'calc(100% - 58%)',
      },
    },
  },
  plugins: [],
};