// import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
// import './App.css';
// import Login from './components/Login';
// import QuizList from './components/QuizList';
// import QuizResult from './components/QuizResult';

// function App() {
//   console.log({Login, QuizList, QuizResult});
//   return (
//     <Router>
//       <Switch>
//         <Route path="/login" component={Login} />
//         <Route path="/quiz" component={QuizList} />
//         <Route path="/result" component={QuizResult} />
//         <Route path="/" exact component={Login} />
//       </Switch>
//     </Router>
//   );
// }

// export default App;
import React, { useState } from 'react';
import QuizQuestion from './components/QuizQuestion';
import QuizResult from './components/QuizResult';
import Login from './components/Login';
import Signup from './components/Signup';
import { Button } from '@mui/material';
import axiosInstance, { getQuizzesApiPath } from './api/axiosConfig';

let questions = [];

export async function login(email, password) {
  try {
    const formData = new URLSearchParams();
    formData.append('email', email);
    formData.append('password', password);

    const response = await axiosInstance.post(getQuizzesApiPath('auth_session/login'), formData, {
      withCredentials: true, // Ensure cookies are included in requests
    });

    console.log('Login successful:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error during login:', error);
    throw error;
  }
}

async function fetchQuizzes() {
  try {
    const response = await axiosInstance.get(getQuizzesApiPath('quizzes'));
    console.log('Quizzes:', response.data);
    questions = response.data;
    return response.data;
  } catch (error) {
    console.error('Error fetching quizzes:', error);
    throw error;
  }
}

fetchQuizzes();

function App() {
  const [user, setUser] = useState(null);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [score, setScore] = useState(0);
  const [isLogin, setIsLogin] = useState(true); // Tracks whether the user is on the login or signup page

  const handleLogin = (userData) => {
    setUser(userData);
    console.log('User logged in:', userData);
  };

  const handleSignup = (userData) => {
    setUser(userData);
    console.log('User signed up:', userData);
  };

  const toggleAuthMode = () => {
    setIsLogin(!isLogin);
  };

  const handleAnswer = (answer) => {
    if (answer === questions[currentQuestion].correctAnswer) {
      setScore(score + 1);
    }
    setCurrentQuestion(currentQuestion + 1);
  };

  return (
    <div className="App">
      {user ? (
        <>
          <h1>Nigerian Geography Trivia</h1>
          {currentQuestion < questions.length ? (
            <QuizQuestion
              question={questions[currentQuestion]}
              onAnswer={handleAnswer}
            />
          ) : (
            <QuizResult score={score} total={questions.length} />
          )}
        </>
      ) : (
        <>
          {isLogin ? (
            <Login onLogin={handleLogin} />
          ) : (
            <Signup onSignup={handleSignup} />
          )}
          <Button onClick={toggleAuthMode}>
            {isLogin ? "Don't have an account? Sign Up" : "Already have an account? Log In"}
          </Button>
        </>
      )}
    </div>
  );
}

export default App;