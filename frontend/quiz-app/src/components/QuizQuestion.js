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