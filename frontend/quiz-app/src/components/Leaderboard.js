import React, { useState, useEffect } from 'react';
import axiosInstance, { getQuizzesApiPath } from '../api/axiosConfig';
import { useParams } from 'react-router-dom';

function Leaderboard() {
  const { id } = useParams();
  const [leaderboard, setLeaderboard] = useState([]);

  useEffect(() => {
    // Fetch the leaderboard data using the API endpoint
    axiosInstance.get(getQuizzesApiPath(`leaderboard/${id}`))
      .then((response) => {
        setLeaderboard(response.data.leaderboard);
      })
      .catch((error) => {
        // Handle error
        console.log('failed to fetch leaderboard!');
      });
  }, [id]);

  return (
    <div>
      <h1>Leaderboard</h1>
      <table>
        <thead>
          <tr>
            <th>Rank</th>
            <th>Score</th>
          </tr>
        </thead>
        <tbody>
          {leaderboard.map((entry, index) => (
            <tr key={index}>
              <td>{index + 1}</td>
              <td>{entry.score}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Leaderboard;