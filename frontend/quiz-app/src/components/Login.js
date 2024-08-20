import React, { useState } from 'react';
import axiosInstance, { getQuizzesApiPath } from '../api/axiosConfig';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = () => {
    // Implement the login functionality using the API endpoint
    axiosInstance.post(getQuizzesApiPath('auth_session/login'), { email, password })
      .then((response) => {
        // Handle successful login
        console.log('logged in successfully!');
      })
      .catch((error) => {
        // Handle login error
        console.log('login failed!');
      });
  };

  return (
    <div>
      <h1>Login</h1>
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
      <button onClick={handleLogin}>Login</button>
    </div>
  );
}

export default Login;