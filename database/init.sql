CREATE DATABASE IF NOT EXISTS mydatabase_name;
USE mydatabase_name;


CREATE TABLE IF NOT EXISTS models (
    id INT AUTO_INCREMENT PRIMARY KEY,
    prompts_name VARCHAR(50),
    prompts TEXT,
    model_name VARCHAR(50) UNIQUE,  -- To ensure that each model name is stored only once (important for the foreign key)
    time_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    total_pages INT,
    metadata TEXT,
    relevant_texts LONGTEXT,
    relevant_pages TEXT,
    model_response TEXT,
    model_name VARCHAR(50),
    time_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (model_name) REFERENCES models(model_name) -- ensures that the model_name in the documents table must exist in the models table.
);
