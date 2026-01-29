export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#667eea',
          dark: '#764ba2',
          light: '#7c96ff',
        },
        accent: {
          green: '#4ade80',
          red: '#f87171',
          yellow: '#fbbf24',
          pink: '#f093fb',
          rose: '#f5576c',
        },
      },
      backgroundImage: {
        'gradient-primary': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'gradient-accent': 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
      },
      boxShadow: {
        'card': '0 5px 15px rgba(0,0,0,0.1)',
        'card-hover': '0 10px 25px rgba(0,0,0,0.15)',
        'section': '0 10px 30px rgba(0,0,0,0.2)',
      },
    },
  },
  plugins: [],
}
