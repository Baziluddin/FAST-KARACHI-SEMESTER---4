-- Q1
SELECT employee_id, first_name, last_name, salary
FROM employees
WHERE salary = (
    SELECT MAX(salary)
    FROM employees
);

-- Q2
SELECT employee_id, first_name, last_name, salary
FROM employees
WHERE salary > (
    SELECT AVG(salary)
    FROM employees
);

-- Q3
SELECT employee_id, first_name, last_name, salary
FROM employees
WHERE salary = (
    SELECT MIN(salary)
    FROM employees
);

-- Q4
SELECT employee_id, first_name, last_name, salary, department_id
FROM employees
WHERE salary = (
    SELECT AVG(salary)
    FROM employees
    WHERE department_id = 20
);

-- Q5
SELECT employee_id, first_name, last_name, hire_date
FROM employees
WHERE hire_date = (
    SELECT MAX(hire_date)
    FROM employees
);

-- Q6
SELECT employee_id, first_name, last_name, department_id
FROM employees
WHERE department_id IN (
    SELECT department_id
    FROM departments
    WHERE location_id = 1700
);

-- Q7
SELECT employee_id, first_name, last_name, job_id
FROM employees
WHERE job_id IN (
    SELECT DISTINCT job_id
    FROM employees
    WHERE department_id = 80
);

-- Q8
SELECT employee_id, first_name, last_name, salary
FROM employees
WHERE salary > ALL (
    SELECT salary
    FROM employees
    WHERE job_id = 'SH_CLERK'
);

-- Q9
SELECT employee_id, first_name, last_name, salary
FROM employees
WHERE salary < ANY (
    SELECT salary
    FROM employees
    WHERE job_id = 'IT_PROG'
);

-- Q10
SELECT employee_id, first_name, last_name, department_id
FROM employees
WHERE department_id IN (
    SELECT department_id
    FROM departments
    WHERE department_name LIKE '%Sales%'
);

-- Q11
SELECT employee_id, first_name, last_name, salary, department_id
FROM employees e
WHERE salary > (
    SELECT AVG(salary)
    FROM employees
    WHERE department_id = e.department_id
);

-- Q12
SELECT employee_id, first_name, last_name, salary, department_id
FROM employees e
WHERE salary = (
    SELECT MAX(salary)
    FROM employees
    WHERE department_id = e.department_id
);

-- Q13
SELECT employee_id, first_name, last_name, salary, job_id
FROM employees e
WHERE salary > (
    SELECT AVG(salary)
    FROM employees
    WHERE job_id = e.job_id
);

-- Q14
SELECT employee_id,
       first_name,
       hire_date,
       department_id
FROM employees e
WHERE hire_date > (
    SELECT MIN(hire_date)
    FROM employees
    WHERE department_id = e.department_id
);

-- Q15
SELECT employee_id, first_name, last_name
FROM employees
WHERE employee_id IN (
    SELECT DISTINCT manager_id
    FROM employees
    WHERE manager_id IS NOT NULL
);

-- Q16
SELECT employee_id, first_name, last_name
FROM employees
WHERE employee_id NOT IN (
    SELECT DISTINCT manager_id
    FROM employees
    WHERE manager_id IS NOT NULL
);

-- Q17
SELECT department_id, department_name
FROM departments d
WHERE NOT EXISTS (
    SELECT 1
    FROM employees e
    WHERE e.department_id = d.department_id
);

-- Q18
SELECT department_id, department_name
FROM departments d
WHERE EXISTS (
    SELECT 1
    FROM employees e
    WHERE e.department_id = d.department_id
      AND e.salary > 10000
);

-- Q19
SELECT department_id, department_name
FROM departments d
WHERE (
    SELECT AVG(salary)
    FROM employees e
    WHERE e.department_id = d.department_id
) > 8000;

-- Q20
SELECT *
FROM (
    SELECT department_id,
           AVG(salary) AS avg_salary
    FROM employees
    GROUP BY department_id
    ORDER BY avg_salary DESC
)
WHERE ROWNUM <= 3;
