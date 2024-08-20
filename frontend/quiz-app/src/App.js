import React from 'react';
import { BrowserRouter as Router, Switch, Route, Link } from 'react-router-dom';
import axiosInstance, { getQuizzesApiPath } from './api/axiosConfig';

import Home from './components/Home';
import Quizzes from './components/Quizzes.js';
import QuizPage from './components/QuizPage';
import Login from './components/Login';
import Signup from './components/Signup';
import Leaderboard from './components/Leaderboard.js';

function App() {
  const handleLogout = () => {
    // Implement the logout functionality using the API endpoint
    axiosInstance.delete(getQuizzesApiPath('auth_session/logout')
      .then((response) => {
        // Handle successful logout
        console.log('logged out successfully!');
      })
      .catch((error) => {
        // Handle logout error
        console.log('logout failed!')
      }));
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

        <Switch>
          <Route path="/quizzes/:id">
            <QuizPage />
          </Route>
          <Route path="/quizzes">
            <Quizzes />
          </Route>
          <Route path="/leaderboard">
            <Leaderboard />
          </Route>
          <Route path="/login">
            <Login />
          </Route>
          <Route path="/signup">
            <Signup />
          </Route>
          <Route path="/">
            <Home />
          </Route>
        </Switch>
      </div>
    </Router>
  );
}

export default App;