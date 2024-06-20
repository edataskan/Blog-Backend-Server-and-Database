create database blog ;
use blog ;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    isim VARCHAR(255) NOT NULL,
    eposta VARCHAR(255) NOT NULL UNIQUE,
    meslek VARCHAR(255)
);

CREATE TABLE posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    baslik VARCHAR(255) NOT NULL,
    aciklama TEXT,
    yorum TEXT,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

