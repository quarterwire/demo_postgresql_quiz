# SQL & RESTful API Template with FastAPI

## Overview
This repository provides a template for working with SQL and RESTful APIs using FastAPI. It demonstrates CRUD operations for a simple quiz system with questions and multiple-choice answers.

## Features
- **FastAPI** framework for building RESTful APIs
- **SQLAlchemy** ORM for database interactions
- **PostgreSQL-compatible** queries
- **Dependency injection** for database management
- **Pydantic** models for data validation

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/sql-fastapi-template.git
   cd demo_postgresql_quiz
   ```
2. **Create and activate a virtual environment:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Set up the database** (ensure PostgreSQL is installed and running):
   ```sh
   alembic upgrade head
   ```
5. **Start the FastAPI server:**
   ```sh
   uvicorn main:app --reload
   ```

## API Endpoints

### Get a Question by ID
```http
GET /questions/{question_id}
```
Retrieves a question by its ID.

### Get Choices for a Question
```http
GET /choices/{question_id}
```
Retrieves all answer choices for a given question.

### Delete a Question
```http
DELETE /questions/{question_id}
```
Deletes a question by its ID.

### Get a Random Question
```http
GET /
```
Returns a randomly selected question.

### Create a New Question
```http
POST /questions/
```
Creates a new question with multiple choices.

## Database Schema

### Questions Table
| Column       | Type    | Description |
|-------------|--------|-------------|
| `id`        | int    | Primary Key |
| `question_text` | string | The question text |

### Choices Table
| Column       | Type    | Description |
|-------------|--------|-------------|
| `id`        | int    | Primary Key |
| `choice_text` | string | The answer choice |
| `is_correct` | boolean | Indicates if the choice is correct |
| `question_id` | int    | Foreign Key referencing `Questions` |

## License
This project is open-source and available under the **MIT License**.

---
### Author
Maintained by **Stoica Ionut**. Contributions are welcome!

