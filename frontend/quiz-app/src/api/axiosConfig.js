import axios from 'axios';

const baseURL = process.env.REACT_APP_API_HOST || 
                (process.env.ENV === 'prod' || process.env.ENV === 'dev'
                ? `https://oga-backend-${process.env.ENV}.onrender.com`
                : 'http://localhost:5000');

const axiosInstance = axios.create({
    baseURL,
    headers: {
        'Content-Type': 'application/json',
    }
});

export const getOrdersApiPath = (path) => `${baseURL}/api/v1/${path}`;

export default axiosInstance;
