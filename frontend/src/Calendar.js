import React, { useState, useEffect, useCallback } from 'react';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
import { fetchEntry, createEntry, logout } from './api';
import { FaGithub, FaLinkedin, FaGlobe } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';

const useAuthStatus = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(() => {
    return localStorage.getItem('isAuthenticated') === 'true';
  });

  useEffect(() => {
    // Listen for changes to localStorage and update state accordingly
    const handleStorageChange = () => {
      setIsAuthenticated(localStorage.getItem('isAuthenticated') === 'true');
    };

    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, []);

  return isAuthenticated;
};

const CalendarPage = () => {
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [description, setDescription] = useState('');
  const [newDescription, setNewDescription] = useState('');
  const isAuthenticated = useAuthStatus();
  const navigate = useNavigate();

  const fetchLearningEntry = useCallback(async () => {
    const formattedDate = selectedDate.toISOString().split('T')[0];
    const entry = await fetchEntry(formattedDate);
    setDescription(entry?.description || "No Entries Yet, Go out and Learn something New!");
  }, [selectedDate]);

  useEffect(() => {
    fetchLearningEntry();
  }, [fetchLearningEntry]);

  const handleCreateEntry = async (e) => {
    e.preventDefault();
    const formattedDate = selectedDate.toISOString().split('T')[0];
    await createEntry(formattedDate, newDescription);
    setNewDescription('');
    fetchLearningEntry(); // Refresh the entry after saving
  };

  const handleLogin = () => {
    navigate('/login');
  };

  const handleLogout = async () => {
    await logout();

    // Clear authentication status
    localStorage.setItem('isAuthenticated', 'false');

    // Clear cookies manually
    document.cookie = 'sessionid=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    document.cookie = 'csrftoken=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';

    window.location.reload();
  };


  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center">
      <nav className="w-full bg-gray-800 text-white py-4 shadow-md">
        <div className="container mx-auto flex justify-between items-center">
          <h1 className="text-xl font-bold">Learning Tracker</h1>
          <div className="flex space-x-4 items-center">
            <a href="https://github.com/yourusername" className="text-gray-400 hover:text-white">
              <FaGithub size={24} />
            </a>
            <a href="https://linkedin.com/in/yourusername" className="text-gray-400 hover:text-white">
              <FaLinkedin size={24} />
            </a>
            <a href="https://yourportfolio.com" className="text-gray-400 hover:text-white">
              <FaGlobe size={24} />
            </a>
            {isAuthenticated ? (
              <button onClick={handleLogout} className="bg-red-500 text-white px-4 py-2 rounded">
                Log Out
              </button>
            ) : (
              <button onClick={handleLogin} className="bg-blue-500 text-white px-4 py-2 rounded">
                Log In
              </button>
            )}
          </div>
        </div>
      </nav>

      <div className="container mx-auto flex flex-col md:flex-row gap-8 p-6 bg-white rounded-lg shadow-lg max-w-4xl mt-8">
        <div className="w-full md:w-1/2">
          <Calendar onChange={setSelectedDate} value={selectedDate} className="border rounded-lg" />
        </div>
        <div className="w-full md:w-1/2">
          <h2 className="text-xl font-semibold mb-4">Learning for {selectedDate.toDateString()}</h2>
          <p className="mb-6">{description}</p>

          {isAuthenticated && (
            <form onSubmit={handleCreateEntry}>
              <textarea
                value={newDescription}
                onChange={(e) => setNewDescription(e.target.value)}
                placeholder="Write what you learned today..."
                className="border p-2 rounded w-full mb-4"
              />
              <button type="submit" className="bg-green-500 text-white px-4 py-2 rounded">
                Save Entry
              </button>
            </form>
          )}
        </div>
      </div>
    </div>
  );
};

export default CalendarPage;
