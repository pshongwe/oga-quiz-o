// import React, { useState } from 'react';
// import { Radio, RadioGroup, FormControlLabel, Button, Typography, Container } from '@mui/material';

// function QuizQuestion({ question, onAnswer }) {
//   const [selectedOption, setSelectedOption] = useState('');

//   const handleSubmit = () => {
//     if (selectedOption) {
//       onAnswer(selectedOption);
//       setSelectedOption('');
//     }
//   };

//   return (
//     <Container maxWidth="sm">
//       <Typography variant="h5" gutterBottom>
//         {question.text}
//       </Typography>
//       <RadioGroup value={selectedOption} onChange={(e) => setSelectedOption(e.target.value)}>
//         {question.options.map((option, index) => (
//           <FormControlLabel
//             key={index}
//             value={option}
//             control={<Radio />}
//             label={option}
//           />
//         ))}
//       </RadioGroup>
//       <Button
//         variant="contained"
//         color="primary"
//         onClick={handleSubmit}
//         disabled={!selectedOption}
//       >
//         Next Question
//       </Button>
//     </Container>
//   );
// }

// export default QuizQuestion;

import React, { useState } from 'react';

function QuizQuestion({ question, onAnswer }) {
  const [selectedOption, setSelectedOption] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (selectedOption) {
      onAnswer(selectedOption);
      setSelectedOption('');
    }
  };

  return (
    <div>
      <h2>{question.text}</h2>
      <form onSubmit={handleSubmit}>
        {question.options.map((option, index) => (
          <div key={index}>
            <input
              type="radio"
              id={option}
              name="answer"
              value={option}
              checked={selectedOption === option}
              onChange={(e) => setSelectedOption(e.target.value)}
            />
            <label htmlFor={option}>{option}</label>
          </div>
        ))}
        <button type="submit">Next</button>
      </form>
    </div>
  );
}

export default QuizQuestion;