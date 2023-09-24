# My Next Gym API

Welcome to the My Next Gym API! This Flask-based backend API provides functionality for managing gym-related information and user interactions. This README will guide you through setting up and using the API.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Usage](#usage)
7. [API Endpoints](#api-endpoints)
8. [Database Models](#database-models)
9. [Frontend Project](#frontend-project)
10. 10. [DEMO](https://www.youtube.com/watch?v=VFmsh5oNHYA)

## Getting Started

These instructions will help you set up and run the backend application on your local machine.

## Features

My Next Gym API offers the following features:

- User registration and authentication
- Gym place creation, retrieval, updating, and deletion
- Workout history tracking
- User-specific gym place and workout history management

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- Python (version 3.7 or higher)
- pip (Python package manager)

## Installation

1. Clone this repository to your local machine:
  ```shell
    git clone <repository-url>

2. Change to the project directory:
  ```shell
    cd <project-directory>


4. Activate the virtual environment:
  - On Windows:
    ```shell```
      venv\Scripts\activate


  - On macOS and Linux:
    ```shell
      source venv/bin/activate


4. Install the required packages:
  ```shell
      pip install -r requirements.txt


## Configuration

Before running the application, make sure to set up your environment variables. Create a `.env` file in the project directory and add the following variables:

- `SECRET_KEY`: A secret key for Flask's session management.
- `SQLALCHEMY_DATABASE_URI`: The URI for your PostgreSQL database.
- `SQLALCHEMY_TEST_DATABASE_URI`: The URI for your test database (if applicable).

By default, the application will run on http://localhost:5000.

## Usage

To get started with the API, follow the installation instructions above. Once the API is up and running, you can use tools like Postman or curl to interact with the routes and enjoy the features provided by this project.

## API Endpoints

Here are the available API endpoints:

### Users

- Register a New User
- **POST** `/user`
- Register a new user account.

- Log in with a Registered User
- **POST** `/user/<username>`
- Log in with a registered user account.

- Get All Users
- **GET** `/user`
- Retrieve information for all users.

- Delete a User
- **DELETE** `/user/<user_id>`
- Delete a user account.

### Gym Places

- Create a New Gym Place
- **POST** `/places`
- Create a new gym place associated with a user.

- Get All Gym Places of a User
- **GET** `/user/<user_id>/places`
- Get all gym places associated with a user.

- Delete Gym Place
- **DELETE** `/places`
- Delete a gym place by its place ID.

### Workout History

- Create a New Workout History Entry
- **POST** `/histories`
- Create a new workout history entry associated with a user.

- Delete Workout History Entry
- **DELETE** `/histories`
- Delete a workout history entry by its history ID.

## Database Models

The application uses SQLAlchemy to interact with the database. Here are the relevant database models:

- **User**: Represents a user with username, password, first name, and last name fields.
- **Place**: Represents a gym place with location details and user association.
- **History**: Represents a workout history entry with date, time spent, mood, and comments fields.

## Frontend Project

You can find the frontend project for My Next Gym on GitHub. The frontend repository contains the user interface and client-side code for interacting with this API.

[Frontend Project on GitHub](https://github.com/doinyco/Frontend-nextgym)


