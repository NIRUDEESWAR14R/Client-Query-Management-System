CREATE DATABASE client_queries;

USE client_queries;

CREATE TABLE queries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255),
    mobile VARCHAR(20),
    query_heading TEXT,
    query_description TEXT,
    query_created_time DATETIME,
    query_closed_time DATETIME,
    status VARCHAR(50)
);

select * from queries;