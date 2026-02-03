
// Check login status on page load
document.addEventListener('DOMContentLoaded', async function() {
    await checkLoginStatus();
    setupAuthForms();
});

// Check if user is logged in
async function checkLoginStatus() {
    try {
        const response = await fetch(`${API_URL}/api/check-session`, {
            credentials: 'include'
        });
        const data = await response.json();
        
        if (data.logged_in) {
            showLoggedInState(data.user);
        } else {
            showLoggedOutState();
        }
    } catch (error) {
        console.error('Error checking session:', error);
        showLoggedOutState();
    }
}

// Show logged in state
function showLoggedInState(user) {
    const authButtons = document.getElementById('authButtons');
    if (authButtons) {
        authButtons.innerHTML = `
            <div class="user-info">
                <span class="username-display">👤 ${user.username}</span>
                <button class="btn-nav btn-logout" onclick="logout()">Logout</button>
            </div>
        `;
    }
    
    // Show recent searches link
    const recentSearchLink = document.getElementById('recentSearchLink');
    if (recentSearchLink) {
        recentSearchLink.style.display = 'inline-block';
    }
}

// Show logged out state
function showLoggedOutState() {
    const authButtons = document.getElementById('authButtons');
    if (authButtons) {
        authButtons.innerHTML = `
            <a href="register.html" class="btn-nav btn-signup">Sign Up</a>
            <a href="login.html" class="btn-nav btn-login">Login</a>
        `;
    }
    
    // Hide recent searches link
    const recentSearchLink = document.getElementById('recentSearchLink');
    if (recentSearchLink) {
        recentSearchLink.style.display = 'none';
    }
}

// Setup auth forms
function setupAuthForms() {
    // Login form
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
    
    // Register form
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }
}

// Handle login
async function handleLogin(e) {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorDiv = document.getElementById('loginError');
    
    try {
        const response = await fetch(`${API_URL}/api/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Redirect to home page
            window.location.href = 'index.html';
        } else {
            errorDiv.textContent = data.message;
            errorDiv.classList.remove('hidden');
        }
    } catch (error) {
        errorDiv.textContent = 'Login failed. Please try again.';
        errorDiv.classList.remove('hidden');
    }
}

// Handle registration
async function handleRegister(e) {
    e.preventDefault();
    
    const username = document.getElementById('regUsername').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('regPassword').value;
    const errorDiv = document.getElementById('registerError');
    const successDiv = document.getElementById('registerSuccess');
    
    try {
        const response = await fetch(`${API_URL}/api/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, email, password })
        });
        
        const data = await response.json();
        
        if (data.success) {
            successDiv.textContent = data.message;
            successDiv.classList.remove('hidden');
            errorDiv.classList.add('hidden');
            
            // Redirect to login after 2 seconds
            setTimeout(() => {
                window.location.href = 'login.html';
            }, 2000);
        } else {
            errorDiv.textContent = data.message;
            errorDiv.classList.remove('hidden');
            successDiv.classList.add('hidden');
        }
    } catch (error) {
        errorDiv.textContent = 'Registration failed. Please try again.';
        errorDiv.classList.remove('hidden');
    }
}

// Logout function
async function logout() {
    try {
        await fetch(`${API_URL}/api/logout`, {
            method: 'POST',
            credentials: 'include'
        });
        
        window.location.href = 'index.html';
    } catch (error) {
        console.error('Logout error:', error);
    }
}