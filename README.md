# Zetech Portal

A comprehensive web-based Zetech Portal built with Flask. This system facilitates the management of academic, administrative, and financial information within a school environment. It supports multiple user roles, including Admin, Finance, and Student, each with tailored dashboards and functionalities.

## Table of Contents

- [Getting Started](#getting-started)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Available Actions](#available-actions)
- [Database Structure](#database-structure)
- [Relationship](#relationship)
- [Dependencies](#dependencies)
- [Contributing](#contributing)

## Getting Started

Welcome to the Zetech Portal! This application is designed to streamline the management of student records, financial accounts, and administrative operations. The system provides a dedicated dashboard for each user role, including Admin, Finance, and Student, to access the relevant information and actions.

## Technologies Used

- **Backend**: Python (Flask)
- **Database**: MySQL (configurable for PostgreSQL or other relational databases)
- **Frontend**: HTML, CSS, Bootstrap, JavaScript
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF
- **ORM**: SQLAlchemy
- **Icons**: Font Awesome

## Installation

To set up and run the project locally, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/RotichKipkoech/zetech-portal.git
    cd zetech-portal
    ```

2. **Create a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database**:
    - Initialize the database by running the following command:
      ```bash
      flask db upgrade
      ```

5. **Run the application**:
    ```bash
    flask run
    ```

6. **Access the application**:
   - Open your web browser and go to [http://localhost:5000](http://localhost:5000).

7. **LIVE LINK**:
   - Open your web browser you can search for deployed link [https://zetech-portal.onrender.com](https://zetech-portal.onrender.com).  
   
   N/B Admin logins are already setup in the Database Username  = Admin Password = Admin@123

## Usage

The application features distinct functionalities for each user role. Login credentials must be created by the Admin, as there is no public sign-up functionality.

### User Roles and Actions

1. **Admin**:
   - Create and manage users (Students, Finance users, etc.).
   - Edit and delete user profiles.
   - Add and update units and classes.
   - Assign financial accounts to students.

2. **Finance**:
   - Manage and update student fees.
   - View financial statements.
   - Process fee payments and monitor outstanding balances.

3. **Student**:
   - View academic records.
   - Access fee balance information.
   - Access current semester timetable, registered units, and social features.

## Available Actions

This system offers a wide range of actions:

- **User Management**: Admin can add, edit, and delete users (students, finance users) with options to set usernames, passwords, and admission/staff numbers.
- **Academic Management**: Admin and Teachers can add units, assign units to students, and manage unit registration status.
- **Financial Management**: Finance users can view all students' financial records, update fee information, and process payments.
- **Student Dashboard**: Students can view their academic progress, unit registration, fee balance, and other relevant information.

## Database Structure

### Key Tables

- **User**: Stores user credentials and basic info (username, password).
- **Student**: Contains student-specific details, including admission numbers.
- **Finance**: Manages finance users and student fee records.
- **Units**: Tracks academic units and their registration status.
  
## Relationship

- **User-Student Relationship**: Each student is associated with a unique User account.
- **Student-Finance Relationship**: Finance records are linked to students for tracking fee balances and payments.
- **Admin and Finance**: Admin has full access to user and finance management, while Finance has access limited to financial transactions and reports.

## Dependencies

The project relies on the following packages:

- **Flask**: Web framework
- **Flask-Login**: User session management
- **Flask-WTF**: Form handling
- **SQLAlchemy**: ORM for database management
- **Bootstrap**: Frontend styling
- **Font Awesome**: Iconography

To install all dependencies:

```bash
pip install -r requirements.txt
