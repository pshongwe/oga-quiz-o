import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import axiosInstance, { getQuizzesApiPath } from './api/axiosConfig';

import './App.css';

import Home from './components/Home';
import Quizzes from './components/Quizzes';
import QuizPage from './components/QuizPage';
import Login from './components/Login';
import Signup from './components/Signup';
import Leaderboard from './components/Leaderboard';

function App() {
  const handleLogout = () => {
    // Implement the logout functionality using the API endpoint
    axiosInstance.delete(getQuizzesApiPath('auth_session/logout'), {}, {
      withCredentials: true,
    })
      .then((response) => {
        // Handle successful logout
        console.log('logged out successfully!');
      })
      .catch((error) => {
        // Handle logout error
        console.log('logout failed!')
      });    
  };

  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
            <li>
              <Link to="/quizzes">Quizzes</Link>
            </li>
            <li>
              <Link to="/leaderboard">Leaderboard</Link>
            </li>
            <li>
              <Link to="/login">Login</Link>
            </li>
            <li>
              <Link to="/signup">Signup</Link>
            </li>
            <li>
              <button onClick={handleLogout}>Logout</button>
            </li>
          </ul>
        </nav>

        <Routes>
          <Route path="/quizzes/:id" element={<QuizPage />} />
          <Route path="/quizzes" element={<Quizzes />} />
          <Route path="/leaderboard" element={<Leaderboard />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/" element={<Home />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;