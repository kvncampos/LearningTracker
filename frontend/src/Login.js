import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { login, fetchCsrfToken } from './api';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        const fetchToken = async () => {
            console.log("Fetching CSRF token on component mount...");
            await fetchCsrfToken();
            console.log("CSRF token fetched");
        };
        fetchToken();
    }, []);

    const handleLogin = async (e) => {
        e.preventDefault();

        // Prevent sending request if fields are empty
        if (!username || !password) {
          setError("Please enter both username and password.");
          return;
        }

        try {
          console.log("Attempting to log in with username:", username);
          const response = await login(username, password);

          if (response) {
            console.log("Login successful!");
            // Set authentication status in localStorage
            localStorage.setItem('isAuthenticated', 'true');
            navigate('/');
          } else {
            setError('Invalid credentials');
          }
        } catch (err) {
          console.error("Error during login:", err);
          setError('Invalid credentials');
        }
      };

    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-100">
            <form onSubmit={handleLogin} className="bg-white p-8 rounded shadow-lg w-96">
                <h2 className="text-2xl font-bold mb-6">Login</h2>
                {error && <p className="text-red-500">{error}</p>}
                <div className="mb-4">
                    <label className="block text-gray-700">Username</label>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        className="w-full p-2 border rounded"
                    />
                </div>
                <div className="mb-4">
                    <label className="block text-gray-700">Password</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className="w-full p-2 border rounded"
                    />
                </div>
                <button type="submit" className="bg-blue-600 text-white py-2 px-4 rounded w-full">
                    Login
                </button>
            </form>
        </div>
    );
};

export default Login;
