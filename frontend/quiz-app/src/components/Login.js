import React, { useState } from 'react';
import { TextField, Button, Container, Typography } from '@mui/material';
import axiosInstance, { getQuizzesApiPath } from '../api/axiosConfig';


function Login({ onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const formData = new URLSearchParams();
      formData.append('email', email);
      formData.append('password', password);

      const response = await axiosInstance.post(getQuizzesApiPath('auth_session/login'), formData, {
        withCredentials: true, // Ensure cookies are included in requests
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded', // Required for form data
        },
      });

      onLogin(response.data);
    } catch (error) {
      console.error('Login failed:', error);
      // Handle login error (e.g., show error message)
    }
  };

  return (
    <Container maxWidth="xs">
      <Typography variant="h4" align="center" gutterBottom>
        Login
      </Typography>
      <form onSubmit={handleSubmit}>
        <TextField
          variant="outlined"
          margin="normal"
          required
          fullWidth
          label="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <TextField
          variant="outlined"
          margin="normal"
          required
          fullWidth
          label="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <Button
          type="submit"
          fullWidth
          variant="contained"
          color="primary"
        >
          Log In
        </Button>
      </form>
    </Container>
  );
}

export default Login;