// const API_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
//     ? 'http://127.0.0.1:5000' 
//     : 'https://movie-reviewer-9nhp.onrender.com';  // Your Render URL

// // Ensure credentials are sent with all requests
// console.log('Using API URL:', API_URL);

const API_URL = window.location.origin + '/api';
console.log('API URL:', API_URL);
// const API_URL =
//   window.location.hostname === 'localhost'
//     ? 'http://127.0.0.1:5000'
//     : 'https://movie-reviewer-9nhp.onrender.com';
// API URL configuration