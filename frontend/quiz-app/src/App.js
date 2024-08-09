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

const questions = [
  {
    text: "What is the capital of Nigeria?",
    options: ["Lagos", "Abuja", "Kano", "Port Harcourt"],
    correctAnswer: "Abuja"
  },
  // Add more questions here
];

function App() {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [score, setScore] = useState(0);

  const handleAnswer = (answer) => {
    if (answer === questions[currentQuestion].correctAnswer) {
      setScore(score + 1);
    }
    setCurrentQuestion(currentQuestion + 1);
  };

  return (
    <div className="App">
      <h1>Nigerian Geography Trivia</h1>
      {currentQuestion < questions.length ? (
        <QuizQuestion
          question={questions[currentQuestion]}
          onAnswer={handleAnswer}
        />
      ) : (
        <QuizResult score={score} total={questions.length} />
      )}
    </div>
  );
}

export default App;