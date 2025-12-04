-- CodeAura Database Schema
-- Run this file to create all necessary tables

CREATE DATABASE IF NOT EXISTS codeaura;
USE codeaura;

-- Students Table
CREATE TABLE students (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(15) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    photo_url VARCHAR(255),
    stream VARCHAR(100),
    age INT,
    joined_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('active', 'inactive', 'graduated') DEFAULT 'active',
    INDEX idx_email (email),
    INDEX idx_phone (phone),
    INDEX idx_status (status)
);

-- Courses Table
CREATE TABLE courses (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(100) NOT NULL,
    fee DECIMAL(10, 2) NOT NULL,
    duration VARCHAR(50),
    image_url VARCHAR(255),
    description LONGTEXT,
    syllabus LONGTEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_type (type),
    INDEX idx_name (name)
);

-- Batches Table
CREATE TABLE batches (
    id INT PRIMARY KEY AUTO_INCREMENT,
    batch_name VARCHAR(255) NOT NULL,
    course_id INT NOT NULL,
    timing VARCHAR(100),
    faculty VARCHAR(255),
    start_date DATE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    INDEX idx_course_id (course_id)
);

-- Enrollments Table
CREATE TABLE enrollments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    batch_id INT NOT NULL,
    status ENUM('active', 'completed', 'dropped') DEFAULT 'active',
    enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (batch_id) REFERENCES batches(id) ON DELETE CASCADE,
    UNIQUE KEY unique_enrollment (student_id, batch_id),
    INDEX idx_student_id (student_id),
    INDEX idx_batch_id (batch_id),
    INDEX idx_status (status)
);

-- Payments Table
CREATE TABLE payments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    method ENUM('razorpay', 'cashfree', 'bank_transfer') DEFAULT 'razorpay',
    receipt_url VARCHAR(255),
    status ENUM('success', 'pending', 'failed') DEFAULT 'pending',
    razorpay_payment_id VARCHAR(255) UNIQUE,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    INDEX idx_student_id (student_id),
    INDEX idx_status (status),
    INDEX idx_payment_date (payment_date)
);

-- Videos Table
CREATE TABLE videos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    course_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    video_url VARCHAR(255) NOT NULL,
    duration INT,
    description LONGTEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    INDEX idx_course_id (course_id)
);

-- Notes Table
CREATE TABLE notes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    course_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    pdf_url VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    INDEX idx_course_id (course_id)
);

-- Tests Table
CREATE TABLE tests (
    id INT PRIMARY KEY AUTO_INCREMENT,
    course_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    questions_json LONGTEXT,
    duration INT,
    passing_score INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    INDEX idx_course_id (course_id)
);

-- Notifications Table
CREATE TABLE notifications (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    message LONGTEXT NOT NULL,
    student_id INT,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    INDEX idx_student_id (student_id),
    INDEX idx_is_read (is_read),
    INDEX idx_created_at (created_at)
);

-- Admins Table
CREATE TABLE admins (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'faculty', 'counsellor') DEFAULT 'admin',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email)
);

-- Sample Data (Optional)

-- Insert sample courses
INSERT INTO courses (name, type, fee, duration, description) VALUES
('Python Full Stack Development', 'Engineering', 15000, '6 months', 'Learn Python, Django, and React'),
('Web Development Bootcamp', 'Engineering', 12000, '3 months', 'HTML, CSS, JavaScript, and beyond'),
('Data Science Masterclass', 'Science', 18000, '4 months', 'Python, ML, and Data Analysis'),
('Mobile App Development', 'Engineering', 14000, '5 months', 'Flutter and React Native');

-- Insert sample batches
INSERT INTO batches (batch_name, course_id, timing, faculty, start_date) VALUES
('Batch A', 1, '10:00 AM - 12:00 PM', 'Mr. Sharma', '2024-01-15'),
('Batch B', 1, '2:00 PM - 4:00 PM', 'Ms. Patel', '2024-01-15'),
('Batch C', 2, '9:00 AM - 11:00 AM', 'Mr. Verma', '2024-01-20'),
('Batch D', 3, '3:00 PM - 5:00 PM', 'Dr. Singh', '2024-01-25');

-- Insert sample admin
INSERT INTO admins (username, email, password_hash, role) VALUES
('admin', 'admin@codeaura.com', 'pbkdf2:sha256:600000$YOUR_HASH_HERE$', 'admin');

-- Note: Password hashes should be generated using werkzeug.security.generate_password_hash()
