-- First, ensure the database exists. If not, run this line:
CREATE DATABASE IF NOT EXISTS microblog;

-- Create a new user named 'user' with the password 'password'
CREATE USER 'user'@'localhost' IDENTIFIED BY 'password';

-- Give this new user all permissions on your application's database
GRANT ALL PRIVILEGES ON microblog.* TO 'user'@'localhost';

-- Apply the changes
FLUSH PRIVILEGES;