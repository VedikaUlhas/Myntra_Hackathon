--create database mydatabase in poetgresql shell
CREATE DATABASE mydatabase;

--Create User Table
CREATE TABLE Users (    user_id SERIAL PRIMARY KEY,    name VARCHAR(100),    email VARCHAR(100),    phone VARCHAR(15));

--Create YouTubeVideos Table
CREATE TABLE YouTubeVideos (    video_id VARCHAR(50) PRIMARY KEY,    title VARCHAR(255),    description TEXT,    view_count INT,    like_count INT,    dislike_count INT,    comment_count INT);

--Create Table
CREATE TABLE YouTubeInteractions (    interaction_id SERIAL PRIMARY KEY,    user_id INT,    video_id VARCHAR(50),    interaction_type VARCHAR(50),    interaction_date TIMESTAMP,    FOREIGN KEY (user_id) REFERENCES Users(user_id),    FOREIGN KEY (video_id) REFERENCES YouTubeVideos(video_id));
