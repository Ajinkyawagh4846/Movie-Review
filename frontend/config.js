// Shared configuration
// Check if in production
const API_URL = window.location.hostname === 'localhost' 
    ? 'http://127.0.0.1:5000' 
    : 'https://movie-reviewer-9nhp.onrender.com';  // Your Render URL
// const API_URL = 'http://127.0.0.1:5000';