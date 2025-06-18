module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: '#3B82F6',
        secondary: '#1F2937',
        dark: {
          100: '#374151',
          200: '#1F2937',
          300: '#111827',
        },
        light: {
          100: '#F9FAFB',
          200: '#F3F4F6',
          300: '#E5E7EB',
        }
      }
    },
  },
  plugins: [],
}