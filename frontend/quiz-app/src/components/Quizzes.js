import React, { useState, useEffect } from 'react';
import axiosInstance, { getQuizzesApiPath } from '../api/axiosConfig';
import { Link } from 'react-router-dom';

function Quizzes() {
  const [quizzes, setQuizzes] = useState([]);

  useEffect(() => {
    // Fetch the list of quizzes using the API endpoint
    axiosInstance.get(getQuizzesApiPath('quizzes'))
      .then((response) => {
        setQuizzes(response.data);
      })
      .catch((error) => {
        // Handle error
        console.log('failed to get quizzes');
      });
  }, []);

  return (
    <div>
      <h1>Quizzes</h1>
      <ul>
        {quizzes.map((quiz) => (
          <li key={quiz._id}>
            <Link to={`/quizzes/${quiz._id}`}>{quiz.title}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Quizzes;