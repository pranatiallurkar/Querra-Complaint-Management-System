-- complaint_system database seed file
-- Run this file in MariaDB to create the schema and sample records.

CREATE DATABASE IF NOT EXISTS complaint_db CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE complaint_db;

DROP TABLE IF EXISTS complaint_updates;
DROP TABLE IF EXISTS complaints;
DROP TABLE IF EXISTS status;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS departments;
DROP TABLE IF EXISTS users;

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

CREATE TABLE complaint_updates (
    update_id INT AUTO_INCREMENT PRIMARY KEY,
    complaint_id INT,
    admin_id INT,
    status_id INT,
    remark TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (complaint_id) REFERENCES complaints(complaint_id) ON DELETE CASCADE,
    FOREIGN KEY (admin_id) REFERENCES users(user_id) ON DELETE SET NULL,
    FOREIGN KEY (status_id) REFERENCES status(status_id) ON DELETE SET NULL
);

INSERT INTO users (name, email, phone, password, role) VALUES
('Alice Kumar', 'alice@email.com', '9876543210', 'pass123', 'customer'),
('Bob Sharma', 'bob@email.com', '9123456780', 'pass123', 'customer');

INSERT INTO departments (dept_name, description) VALUES
('IT Support', 'Technical support for hardware and software issues'),
('HR', 'Human resources and employee support'),
('Facilities', 'Campus and facility maintenance');

INSERT INTO categories (category_name, dept_id) VALUES
('Laptop Issue', 1),
('Network Issue', 1),
('Payroll Issue', 2),
('Policy Question', 2),
('Maintenance Request', 3);

INSERT INTO status (status_name) VALUES
('Open'),
('In Progress'),
('Resolved');

INSERT INTO complaints (user_id, dept_id, category_id, status_id, title, description, priority) VALUES
(1, 1, 1, 1, 'Laptop not working', 'My laptop will not boot and shows a black screen.', 'High'),
(2, 1, 2, 2, 'Wi-Fi disconnects often', 'The campus Wi-Fi loses connection every 10 minutes.', 'Medium'),
(1, 2, 3, 1, 'Salary not credited', 'My monthly salary has not been received in my bank account.', 'High');
