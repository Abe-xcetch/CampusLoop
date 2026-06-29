/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,jsx,ts,tsx}",
    "./src/**/*.{js,jsx,ts,tsx}",
    "../../packages/ui/src/**/*.{js,jsx,ts,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        strathmore: {
          blue: {
            DEFAULT: "#003366",
            light: "#004080",
            dark: "#002244",
          },
          gold: {
            DEFAULT: "#cc9933",
            light: "#d6ad5c",
            dark: "#ad7d1f",
          }
        }
      }
    },
  },
  plugins: [],
}
