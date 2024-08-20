// components/QuizPage.js
import React, { useState, useEffect } from 'react';
import axiosInstance, { getQuizzesApiPath } from '../api/axiosConfig';
import { useParams } from 'react-router-dom';

function QuizPage() {
  const { id } = useParams();
  const [quiz, setQuiz] = useState(null);
  const [sessionId, setSessionId] = useState('');
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [userAnswer, setUserAnswer] = useState('');
  const [score, setScore] = useState(0);

  useEffect(() => {
    // Fetch the quiz details using the API endpoint
    axiosInstance.get(getQuizzesApiPath(`quizzes/${id}`))
      .then((response) => {
        setQuiz(response.data);
      })
      .catch((error) => {
        // Handle error
        console.log(`failed to get quiz id: ${id}`)
      });

    // Start a new quiz session using the API endpoint
    axiosInstance.post(getQuizzesApiPath(`quizzes/${id}/start`))
      .then((response) => {
        setSessionId(response.data.session_id);
      })
      .catch((error) => {
        // Handle error
        console.log(`failed to start quiz id: ${id}`)
      });
  }, [id]);

  const handleAnswerSubmit = () => {
    // Submit the user's answer using the API endpoint
    axiosInstance.put(getQuizzesApiPath(`quizzes/session/${sessionId}`), { answer: userAnswer })
      .then((response) => {
        if (response.data.correct) {
          setScore(score + 1);
        }
        setCurrentQuestion(currentQuestion + 1);
        setUserAnswer('');
      })
      .catch((error) => {
        // Handle error
        console.log('failed to handle answer submit!');
      });
  };

  if (!quiz) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>{quiz.title}</h1>
      <p>{quiz.questions[currentQuestion].question}</p>
      <input
        type="text"
        value={userAnswer}
        onChange={(e) => setUserAnswer(e.target.value)}
      />
      <button onClick={handleAnswerSubmit}>Submit</button>
      <p>Score: {score}</p>
    </div>
  );
}

export default QuizPage;