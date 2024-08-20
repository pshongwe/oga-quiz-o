import React, { useState } from 'react';
import axiosInstance, { getQuizzesApiPath } from '../api/axiosConfig';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = () => {
    try {
      const formData = new URLSearchParams();
      formData.append('email', email);
      formData.append('password', password);

      axiosInstance.post(getQuizzesApiPath('auth_session/login'), formData, {
        withCredentials: false, // Ensure cookies are included in requests
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded', // Required for form data
        },
      }).then((response) => {
        // Handle successful signup
        console.log('login success!');
      })
      .catch((error) => {
        // Handle signup error
        console.log('login failed!');
      });
    } catch (error) {
      console.error('Login failed before try:', error);
      // Handle login error (e.g., show error message)
    }

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