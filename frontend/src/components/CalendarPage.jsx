import { useEffect, useState } from 'react';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL;

const CalendarPage = () => {
  const [entries, setEntries] = useState([]);
  const today = new Date().toISOString().split('T')[0]; // Today's date in YYYY-MM-DD format

  useEffect(() => {
    const fetchEntries = async () => {
      try {
        const response = await fetch(
          `${API_BASE_URL}/api/learned-entries/?date=${today}`,
          {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': getCookie('csrftoken'),
            },
            credentials: 'include', // Include cookies for authentication
          }
        );

        if (response.ok) {
          const data = await response.json();
          setEntries(data);
        } else {
          console.error('Failed to fetch entries');
        }
      } catch (error) {
        console.error('Error fetching entries:', error);
      }
    };

    fetchEntries();
  }, [today]);

  const getCookie = (name) => {
    const cookies = document.cookie.split('; ');
    const cookie = cookies.find((row) => row.startsWith(name));
    return cookie?.split('=')[1];
  };

  return (
    <div className='max-w-7xl mx-auto p-4'>
      <h1 className='text-2xl font-bold mb-4'>Learning Calendar</h1>
      <p className='text-lg mb-4'>Entries for {today}:</p>
      <ul>
        {entries.map((entry) => (
          <li key={entry.id}>
            <strong>{entry.learning_type}</strong>: {entry.description}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CalendarPage;
