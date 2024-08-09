// import React from 'react';
// import { Typography, Container, Button } from '@mui/material';

// function QuizResult({ score, totalQuestions, onRetry }) {
//   const percentage = (score / totalQuestions) * 100;

//   return (
//     <Container maxWidth="sm">
//       <Typography variant="h4" align="center" gutterBottom>
//         Quiz Results
//       </Typography>
//       <Typography variant="h5" align="center" gutterBottom>
//         Your Score: {score} / {totalQuestions}
//       </Typography>
//       <Typography variant="h6" align="center" gutterBottom>
//         Percentage: {percentage.toFixed(2)}%
//       </Typography>
//       <Typography variant="body1" align="center" paragraph>
//         {percentage >= 70
//           ? "Great job! You're a Nigerian geography expert!"
//           : "Keep learning about Nigerian geography and try again!"}
//       </Typography>
//       <Button
//         variant="contained"
//         color="primary"
//         fullWidth
//         onClick={onRetry}
//       >
//         Try Again
//       </Button>
//     </Container>
//   );
// }

// export default QuizResult;

import React from 'react';

function QuizResult({ score, total }) {
  return (
    <div>
      <h2>Quiz Completed!</h2>
      <p>Your score: {score} out of {total}</p>
    </div>
  );
}

export default QuizResult;