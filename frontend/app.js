const express = require('express');
const axios = require('axios');
const path = require('path');

const app = express();

// Read API URL from environment variable (fallback for local dev)
const API_URL = process.env.API_URL || 'http://api:8000';

app.use(express.json());
app.use(express.static(path.join(__dirname, 'views')));

// Health check endpoint for Docker HEALTHCHECK
app.get('/health', (req, res) => {
  res.status(200).send('ok');
});

app.post('/submit', async (req, res) => {
  try {
    const response = await axios.post(`${API_URL}/jobs`);
    res.json(response.data);
  } catch (err) {
    console.error('Error submitting job:', err.message);
    res.status(500).json({ error: 'Failed to submit job' });
  }
});

app.get('/status/:id', async (req, res) => {
  try {
    const response = await axios.get(`${API_URL}/jobs/${req.params.id}`);
    res.json(response.data);
  } catch (err) {
    console.error('Error fetching job status:', err.message);
    res.status(500).json({ error: 'Failed to fetch job status' });
  }
});

const server = app.listen(3000, '0.0.0.0', () => {
  console.log('Frontend running on port 3000');
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM received, closing server...');
  server.close(() => {
    console.log('Server closed');
    process.exit(0);
  });
});