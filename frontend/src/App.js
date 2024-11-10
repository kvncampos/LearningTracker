import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LearningCalendar from './Calendar';
import Login from './Login';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LearningCalendar />} />
        <Route path="/login" element={<Login />} />
      </Routes>
    </Router>
  );
}

export default App;
