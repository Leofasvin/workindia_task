# Railway Management System

## Overview

This project is a basic railway management system using Python Flask and PostgreSQL. It allows users to register, log in, check train availability, and book seats. Admins can add new trains and manage seat availability.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x
- PostgreSQL database

## Installation

### 1. Clone the Repository

First, clone the repository to your local machine:
bash
```
git clone <repository_url>
cd <repository_directory>
```
### 2. Set Up a Virtual Environment
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install Required Packages
```
pip install -r requirements.txt
```
4. Configure the Database
```
CREATE DATABASE railway_db;
CREATE USER your_username WITH PASSWORD 'your_password';
ALTER ROLE your_username SET client_encoding TO 'utf8';
ALTER ROLE your_username SET default_transaction_isolation TO 'read committed';
ALTER ROLE your_username SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE railway_db TO your_username;
```
5. Set Up Database Tables
```
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    role VARCHAR(20) CHECK (role IN ('admin', 'user')) NOT NULL
);

CREATE TABLE trains (
    id SERIAL PRIMARY KEY,
    source VARCHAR(50) NOT NULL,
    destination VARCHAR(50) NOT NULL,
    total_seats INT NOT NULL,
    available_seats INT NOT NULL
);

CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    train_id INT REFERENCES trains(id),
    seats_booked INT NOT NULL
);
```
6. Configure the Flask Application
```
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://your_username:your_password@localhost:5432/railway_db'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
```
7. Running the Application
```
python app.py
```


