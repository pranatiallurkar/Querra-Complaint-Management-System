# Complaint System

A beginner-friendly complaint management dashboard built with Flask, MariaDB/MySQL, and plain HTML/CSS/JavaScript.

## What is included

- Modern dashboard UI with sidebar, summary cards, search, filters, and responsive design
- Add complaint form with dynamic department/category dropdowns and validation
- Complaint listing page with status/priority filters and live refresh
- Flask REST APIs for departments, categories, users, status, and complaints
- MariaDB connection helper and JSON API responses
- Dark/modern dashboard styling with Font Awesome icons

## Files

- `backend/app.py` — Flask server, API routes, and static page routing
- `backend/db_connect.py` — MariaDB connection helper
- `frontend/index.html` — Dashboard homepage
- `frontend/add_complaint.html` — Complaint submission page
- `frontend/complaints.html` — Complaint table and filters
- `static/style.css` — Modern dashboard styling
- `requirements.txt` — Python dependencies

## Setup

1. Clone or open the project in VS Code.
2. Create a Python virtual environment and activate it:

```powershell
cd C:\Users\prana\OneDrive\Desktop\complaint_system
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Configure the database connection in `backend/db_connect.py`:

```python
config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'database': 'complaint_db',
    'raise_on_warnings': True,
    'autocommit': True,
}
```

5. Create the database and tables in MariaDB before running.

## Database Schema

Use this schema for `complaint_db`:

```sql
CREATE DATABASE IF NOT EXISTS complaint_db CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE complaint_db;

CREATE TABLE users (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(100),
  phone VARCHAR(20),
  password VARCHAR(100),
  role VARCHAR(20)
);

CREATE TABLE departments (
  dept_id INT AUTO_INCREMENT PRIMARY KEY,
  dept_name VARCHAR(100),
  description TEXT
);

CREATE TABLE categories (
  category_id INT AUTO_INCREMENT PRIMARY KEY,
  category_name VARCHAR(100),
  dept_id INT,
  FOREIGN KEY (dept_id) REFERENCES departments(dept_id) ON DELETE SET NULL
);

CREATE TABLE status (
  status_id INT AUTO_INCREMENT PRIMARY KEY,
  status_name VARCHAR(50)
);

CREATE TABLE complaints (
  complaint_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT,
  dept_id INT,
  category_id INT,
  status_id INT,
  title VARCHAR(255),
  description TEXT,
  priority VARCHAR(20),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL,
  FOREIGN KEY (dept_id) REFERENCES departments(dept_id) ON DELETE SET NULL,
  FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE SET NULL,
  FOREIGN KEY (status_id) REFERENCES status(status_id) ON DELETE SET NULL
);
```

## Seed data example

```sql
INSERT INTO users (name, email, phone, password, role)
VALUES ('Alice Kumar', 'alice@email.com', '9876543210', 'pass123', 'customer');

INSERT INTO departments (dept_name, description)
VALUES ('IT Support', 'Technical support'), ('HR', 'Employee issues');

INSERT INTO categories (category_name, dept_id)
VALUES ('Laptop Issue', 1), ('Network Issue', 1), ('Salary Issue', 2);

INSERT INTO status (status_name)
VALUES ('Open'), ('In Progress'), ('Resolved');

INSERT INTO complaints (user_id, dept_id, category_id, status_id, title, description, priority)
VALUES (1, 1, 1, 1, 'Laptop not working', 'Laptop not booting', 'high');
```

## Run the app

```powershell
cd backend
python app.py
```

Open:

- `http://localhost:5000/`
- `http://localhost:5000/add`
- `http://localhost:5000/complaints`

## Notes

- The app serves HTML pages and API endpoints from the same Flask backend.
- If you change the database credentials, update `backend/db_connect.py`.
- The frontend uses `/assets/style.css` to load the stylesheet.
