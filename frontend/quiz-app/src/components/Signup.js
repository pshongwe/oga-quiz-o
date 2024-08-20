import React, { useState } from 'react';
import axiosInstance, { getQuizzesApiPath } from '../api/axiosConfig';

function Signup() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSignup = () => {
    const formData = new URLSearchParams();
    formData.append('email', email);
    formData.append('password', password);
    // Implement the signup functionality using the API endpoint
    axiosInstance.post(getQuizzesApiPath('auth_session/signup'), formData, {
      withCredentials: false, // Ensure cookies are included in requests
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded', // Required for form data
      },
    }).then((response) => {
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