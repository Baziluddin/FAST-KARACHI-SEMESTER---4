-- Q1
CREATE TABLE Employees (
    emp_id VARCHAR2(10) PRIMARY KEY,
    emp_name VARCHAR2(50),
    age NUMBER,
    salary NUMBER,
    join_date DATE
);

-- Q2
ALTER TABLE Employees
MODIFY emp_name VARCHAR2(100);

-- Q3
ALTER TABLE Employees
ADD email VARCHAR2(100);

-- Q4
ALTER TABLE Employees
ADD CONSTRAINT emp_email_uk UNIQUE (email);

-- Q5
ALTER TABLE Employees
ADD CONSTRAINT emp_age_ck CHECK (age >= 18);

-- Q6
INSERT INTO Employees
VALUES ('E001', 'Ali Khan', 25, 50000, DATE '2024-01-10', 'ali@gmail.com');

INSERT INTO Employees
VALUES ('E002', 'Ahmed Raza', 30, 60000, DATE '2023-05-15', 'ahmed@gmail.com');

INSERT INTO Employees
VALUES ('E003', 'Sara Ahmed', 28, 55000, DATE '2022-08-20', 'sara@gmail.com');

INSERT INTO Employees
VALUES ('E004', 'Fatima Noor', 35, 70000, DATE '2021-03-12', 'fatima@gmail.com');

INSERT INTO Employees
VALUES ('E005', 'Usman Ali', 24, 45000, DATE '2024-07-01', 'usman@gmail.com');

-- Q7
INSERT INTO Employees
VALUES ('E006', 'Young Employee', 16, 30000, DATE '2025-01-01', 'young@gmail.com');

-- Q8
INSERT INTO Employees
VALUES ('E007', 'Duplicate Email', 26, 40000, DATE '2025-02-01', 'ali@gmail.com');

-- Q9
DELETE FROM Employees
WHERE emp_id = 'xyz';

ROLLBACK;

-- Q10
DELETE FROM Employees;
