import React, { useState } from 'react';
import axiosInstance, { getQuizzesApiPath } from '../api/axiosConfig';

function Signup() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSignup = () => {
    // Implement the signup functionality using the API endpoint
    axiosInstance.post(getQuizzesApiPath('auth_session/signup'), { email, password })
      .then((response) => {
        // Handle successful signup
        console.log('signup success!');
      })
      .catch((error) => {
        // Handle signup error
        console.log('signup failed!');
      });
  };

  return (
    <div>
      <h1>Signup</h1>
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button onClick={handleSignup}>Signup</button>
    </div>
  );
}

export default Signup;