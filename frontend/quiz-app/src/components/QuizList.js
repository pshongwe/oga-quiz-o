import { useEffect, useState } from 'react';
import axios from 'axios';


function QuizList() {
  const [quizzes, setQuizzes] = useState([]);

  useEffect(() => {
    axios.get('/api/v1/quizzes')
      .then(response => setQuizzes(response.data))
      .catch(error => console.error('Error fetching quizzes:', error));
  }, []);

  // Render quizzes
}

export default QuizList;