export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#2563eb',
          dark: '#1e40af',
          light: '#3b82f6',
        },
        accent: {
          blue: '#2563eb',
          cyan: '#06b6d4',
          green: '#10b981',
          red: '#ef4444',
          yellow: '#f59e0b',
        },
      },
      backgroundImage: {
        'gradient-primary': 'linear-gradient(135deg, #2563eb 0%, #1e40af 100%)',
        'gradient-blue': 'linear-gradient(135deg, #2563eb 0%, #06b6d4 100%)',
      },
      boxShadow: {
        'brutal': '8px 8px 0px 0px rgba(0,0,0,1)',
        'brutal-sm': '4px 4px 0px 0px rgba(0,0,0,1)',
        'brutal-lg': '12px 12px 0px 0px rgba(0,0,0,1)',
      },
      borderWidth: {
        '3': '3px',
        '4': '4px',
      },
    },
  },
  plugins: [],
}
