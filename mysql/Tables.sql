-- This command is needed to select the correct database first
USE microblog;

-- 1. Creates the 'users' table
CREATE TABLE users (
    id INT AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (username)
);

-- 2. Creates the 'posts' table with a foreign key to the users table
CREATE TABLE posts (
    id INT AUTO_INCREMENT,
    text VARCHAR(64) NOT NULL,
    owner_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY(owner_id) REFERENCES users(id)
);

-- 3. Creates the 'followers' association table
-- This table tracks the many-to-many relationship of who follows whom
CREATE TABLE followers (
    follower_id INT NOT NULL,
    followed_id INT NOT NULL,
    PRIMARY KEY (follower_id, followed_id),
    FOREIGN KEY(follower_id) REFERENCES users(id),
    FOREIGN KEY(followed_id) REFERENCES users(id)
);