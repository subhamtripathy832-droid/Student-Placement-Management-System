CREATE DATABASE IF NOT EXISTS placement_db
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE placement_db;

-- This SQL schema mirrors the SQLAlchemy models in models.py.
-- The recommended setup path is: create the database, then run python init_db.py.
-- This file is provided as a readable database-design reference.

CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(120) NOT NULL,
    email VARCHAR(160) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    department VARCHAR(100),
    graduation_year INT,
    cgpa DECIMAL(4,2),
    role VARCHAR(20) NOT NULL DEFAULT 'student',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_students_email (email)
);

CREATE TABLE IF NOT EXISTS companies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(160) NOT NULL UNIQUE,
    website VARCHAR(255),
    description TEXT,
    location VARCHAR(160),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    company_id INT NOT NULL,
    title VARCHAR(160) NOT NULL,
    description TEXT NOT NULL,
    location VARCHAR(160),
    minimum_cgpa DECIMAL(4,2) DEFAULT 0,
    eligible_departments VARCHAR(255) DEFAULT 'All',
    graduation_year INT,
    deadline DATE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT fk_jobs_company FOREIGN KEY (company_id) REFERENCES companies(id)
);

CREATE TABLE IF NOT EXISTS applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    job_id INT NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'Submitted',
    applied_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_applications_student FOREIGN KEY (student_id) REFERENCES students(id),
    CONSTRAINT fk_applications_job FOREIGN KEY (job_id) REFERENCES jobs(id),
    CONSTRAINT uq_student_job_application UNIQUE (student_id, job_id)
);

CREATE TABLE IF NOT EXISTS placement_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    company_id INT NOT NULL,
    job_title VARCHAR(160) NOT NULL,
    package_lpa DECIMAL(8,2),
    placement_date DATE,
    CONSTRAINT fk_placements_student FOREIGN KEY (student_id) REFERENCES students(id),
    CONSTRAINT fk_placements_company FOREIGN KEY (company_id) REFERENCES companies(id)
);
