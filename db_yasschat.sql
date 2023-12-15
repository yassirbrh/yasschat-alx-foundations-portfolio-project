-- Create YassChat Database
CREATE DATABASE IF NOT EXISTS YassChat;
USE YassChat;

-- Create User Table
CREATE TABLE IF NOT EXISTS User (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(255) NOT NULL,
    FullName VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Created_At DATETIME DEFAULT CURRENT_TIMESTAMP,
    Last_Active DATETIME
);

-- Create Friendship Table
CREATE TABLE IF NOT EXISTS Friendship (
    FriendshipID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    FriendID INT,
    isAccepted BOOLEAN,
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (FriendID) REFERENCES User(UserID)
);

-- Create Message Table
CREATE TABLE IF NOT EXISTS Message (
    MessageID INT AUTO_INCREMENT PRIMARY KEY,
    SenderID INT,
    ReceiverID INT,
    Message VARCHAR(255) NOT NULL,
    Timestamp DATETIME NOT NULL,
    isRead BOOLEAN,
    FOREIGN KEY (SenderID) REFERENCES User(UserID),
    FOREIGN KEY (ReceiverID) REFERENCES User(UserID)
);
