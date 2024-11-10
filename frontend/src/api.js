import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000',
    withCredentials: true,  // IMPORTANT: This allows cookies to be sent
});

// Fetch CSRF token from cookies
const getCsrfToken = () => {
    console.log("Fetching CSRF token from cookies...");
    const cookies = document.cookie;
    console.log("Cookies found:", cookies);

    const csrfCookie = cookies
        .split('; ')
        .find(row => row.startsWith('csrftoken='));

    console.log("CSRF Cookie:", csrfCookie);
    const csrfToken = csrfCookie ? csrfCookie.split('=')[1] : null;
    console.log("CSRF Token extracted:", csrfToken);
    return csrfToken;
};

// Axios request interceptor to add CSRF token to headers
api.interceptors.request.use(config => {
    const csrfToken = getCsrfToken();
    if (csrfToken) {
        config.headers['X-CSRFToken'] = csrfToken;
    }
    return config;
}, error => Promise.reject(error));

// Fetch CSRF token on app load
export const fetchCsrfToken = async () => {
    try {
        console.log("Fetching CSRF token from /api/get-csrf-token/");
        await api.get('/api/get-csrf-token/');
        console.log("CSRF token fetch successful");
    } catch (error) {
        console.error('Error fetching CSRF token:', error);
    }
};

// Example: Login request
export const login = async (username, password) => {
    try {
        const response = await api.post('/api/login/', { username, password });
        return response.data;
    } catch (error) {
        console.error('Login failed:', error);
        return null;
    }
};

// Example: Logout request
export const logout = async () => {
    try {
        const response = await api.post('/api/logout/');
        return response.data;
    } catch (error) {
        console.error('Logout failed:', error);
        return null;
    }
};

// Example: Fetch entry
export const fetchEntry = async (date) => {
    try {
        const response = await api.get(`/api/entry/?date=${date}`);
        return response.data;
    } catch (error) {
        console.error('Error fetching entry:', error);
        return null;
    }
};

// Example: Create or update entry
export const createEntry = async (date, description) => {
    try {
        const response = await api.post('/api/entry/', { date, description });
        return response.data;
    } catch (error) {
        console.error('Error creating entry:', error);
        return null;
    }
};

export default api;
