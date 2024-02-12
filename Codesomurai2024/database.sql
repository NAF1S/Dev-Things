DROP TABLE IF EXISTS User;

CREATE TABLE User(
    user_id INTEGER NOT NULL,
    user_name varchar(255),
    balance INTEGER
);

DROP TABLE IF EXISTS Station;
CREATE TABLE Station(
    station_id INTEGER NOT NULL,
    station_name varchar(255),
    longitude float,
    latitude float
);


DROP TABLE IF EXISTS Trains;
-- Table to store train information
CREATE TABLE Trains (
    train_id INT PRIMARY KEY,
    train_name VARCHAR(100),
    capacity INT
);

-- Table to store stations for each train
DROP TABLE IF EXISTS Stations;
CREATE TABLE Stations (
    station_id INT PRIMARY KEY,
    train_id INT,
    arrival_time TIME,
    departure_time TIME,
    fare INTEGER,
    FOREIGN KEY (train_id) REFERENCES Trains(train_id)
);
