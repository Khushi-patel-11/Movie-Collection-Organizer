# CREATE TABLE Movies (
#     movie_id INT AUTO_INCREMENT PRIMARY KEY,
#     movie_name VARCHAR(255),
#     released_year INT,
#     genre VARCHAR(100),
#     duration INT
# );
# CREATE TABLE Actors (
#     actor_id INT AUTO_INCREMENT PRIMARY KEY,
#     actor_name VARCHAR(255) NOT NULL,
#     birth_date DATE NOT NULL,
#     gender ENUM('Male', 'Female', 'Other') NOT NULL
# );
# CREATE TABLE Movie_Actor (
#     movie_id INT NOT NULL,
#     actor_id INT NOT NULL,
#     PRIMARY KEY (movie_id, actor_id),
#     FOREIGN KEY (movie_id) REFERENCES Movies(movie_id) ON DELETE CASCADE,
#     FOREIGN KEY (actor_id) REFERENCES Actors(actor_id) ON DELETE CASCADE
# );
# CREATE TABLE Directors (
#     director_id INT AUTO_INCREMENT PRIMARY KEY,
#     director_name VARCHAR(255) NOT NULL,
#     birth_date DATE NOT NULL,
#     gender varchar(45) NOT NULL
# );
# CREATE TABLE Users (
#     user_id INT AUTO_INCREMENT PRIMARY KEY,
#     user_name VARCHAR(255) NOT NULL,
#     user_email VARCHAR(255) NOT NULL UNIQUE,
#     password VARCHAR(255) NOT NULL 
# );
# CREATE TABLE User_Rating (
#     rating_id INT AUTO_INCREMENT PRIMARY KEY,
#     user_id INT NOT NULL,
#     movie_id INT NOT NULL,
#     rating DECIMAL(2, 1) NOT NULL CHECK (rating >= 0 AND rating <= 10),
#     FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
#     FOREIGN KEY (movie_id) REFERENCES Movies(movie_id) ON DELETE CASCADE
# );
# CREATE TABLE movie_director (
#     movie_id INT,
#     director_id INT,
#     PRIMARY KEY (movie_id, director_id),
#     FOREIGN KEY (movie_id) REFERENCES Movies(movie_id) ON DELETE CASCADE,
#     FOREIGN KEY (director_id) REFERENCES Directors(director_id) ON DELETE CASCADE
# );
