-- Maak de database
CREATE DATABASE Test;

USE Test;

-- Tabel: power
CREATE TABLE Power(
    power_id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp_data DATETIME DEFAULT CURRENT_TIMESTAMP,
    power_value INT
);

CREATE TABLE Voltage(
    volt_id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp_data DATETIME DEFAULT CURRENT_TIMESTAMP,
    volt_value INT
);

INSERT INTO
    Power (power_value)VALUES 
    (1),(2),(3),(4),(5),(6);


INSERT INTO Voltage(volt_value) VALUES
(10), (20), (40), (5), (73), (18), (44), (42);