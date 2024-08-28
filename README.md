
# Oga Quiz O API

This repository contains the backend API for the Oga Quiz O application. The API is built using Flask, Flask-RESTX, and MongoDB, providing functionalities for user authentication and quiz management.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Environment Variables](#environment-variables)
- [License](#license)

## Features

- User Signup and Login with secure password hashing.
- JWT-based authentication.
- CRUD operations for quizzes.
- Leaderboard and score tracking for quizzes.
- RESTful API with detailed Swagger documentation.

## Installation

### Prerequisites

- Python 3.12+
- MongoDB
- [pip](https://pip.pypa.io/en/stable/) (Python package manager)

### Clone the Repository

```bash
git clone https://github.com/yourusername/oga-quiz-o-api.git
cd oga-quiz-o-api
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the root directory of your project and add the following environment variables:

```env
MY_SECRET=your_secret_key
API_HOST=0.0.0.0
API_PORT=5000
MONGO_URI=mongodb://localhost:27017/oga_db
```

### Run the Application

```bash
python app.py
```

The API will be available at `http://localhost:5000`.

## Usage

### Running the Application

To start the backend application (within the backend folder), run:

```bash
podman compose up
```

To start the frontend application (within the frontend/quiz-app folder), run:

```bash
npm start
```

## API Documentation

The API documentation is available via Swagger at:

```
http://localhost:5000/swagger/
```

This provides detailed information on all available endpoints, request/response formats, and data models.

## Project Structure

```bash
oga-quiz-o-api/
│
├── api/
│   ├── v1/
│   │   ├── __init__.py
│   │   ├── views.py
│   │   ├── auth/
│   │   │   └── auth.py
│
├── libs/
│   ├── __init__.py
│   └── db.py
│
├── tests/
│   ├── __init__.py
│   └── test_app.py
│
├── app.py
├── requirements.txt
└── README.md
```

- `api/v1/`: Contains all the API-related code.
- `libs/`: Contains utility modules, including the database connection and helpers.
- `tests/`: Contains unit tests for the application.
- `app.py`: The main application entry point.
- `requirements.txt`: A list of Python packages required by the project.

## Environment Variables

This project uses environment variables for configuration. The main variables are:

- `MY_SECRET`: Secret key for session management.
- `API_HOST`: The host address for the API.
- `API_PORT`: The port for the API.
- `MONGO_URI`: Connection string for MongoDB.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
