-- Maak de database
CREATE DATABASE Dummydata;

USE Dummydata;

-- Tabel: power
CREATE TABLE Power(
    power_id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp_data DATETIME,
    power_value INT
);
INSERT INTO
    Power(power_value)
VALUES (523),
    (874),
    (120),
    (967),
    (50),
(833),
(678),
(650),
(704),
(286),
(18),
(839),
(100),
(340),
(630),
(643),
(32),
(91),
(447),
(276),
(322),
(759),
(247),
(743);

INSERT INTO PowerWeek(powerW_value) VALUES
(733),
(516),
(209),
(290),
(523),
(67),
(123);

CREATE TABLE PowerWeek(
    power_id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp_data DATETIME DEFAULT CURRENT_TIMESTAMP,
    powerW_value INT
);

INSERT into PowerMonth(powerM_value) VALUES
( 986),
(754),
( 866),
(382),
(957),
(797),
(679),
(372),
( 239),
( 36),
( 463),
( 83),
( 719),
( 318),
( 827),
( 259),
(445),
( 835),
(497),
(694),
(681),
(885),
( 127),
( 479),
(716),
( 800),
(64),
( 642),
( 231),
( 620),
( 15);


CREATE TABLE PowerMonth(
    power_id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp_data DATETIME DEFAULT CURRENT_TIMESTAMP,
    powerM_value INT
);

INSERT into PowerYear(powerY_value) VALUES
(694),
(681),
(885),
(127),
(479),
(716),
(800),
(64),
(642),
(231),
(620),
(15);

CREATE TABLE PowerYear(
    power_id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp_data DATETIME DEFAULT CURRENT_TIMESTAMP,
    powerY_value INT
);

CREATE TABLE Voltage (
    volt_id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp_data DATETIME DEFAULT CURRENT_TIMESTAMP,
    volt_value INT
);

INSERT into Voltage (volt_value) VALUES
( 83),
( 539),
( 171),
( 940),
( 510),
(792),
( 566),
( 799),
( 932),
( 51),
( 718),
( 678),
(94),
( 833),
( 177),
( 385),
( 476),
( 788),
(767),
(625),
( 731),
(246),
(705),
(942);

CREATE TABLE VoltWeek (
    volt_id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp_data DATETIME DEFAULT CURRENT_TIMESTAMP,
    voltW_value INT
);

INSERT INTO
    VoltWeek (timestamp_data, voltW_value)
VALUES ('2025-11-01 10:00:00', 733),
    ('2025-11-02 10:00:00', 516),
    ('2025-11-03 10:00:00', 209),
    ('2025-11-04 10:00:00', 290),
    ('2025-11-05 10:00:00', 523),
    ('2025-11-06 10:00:00', 67),
    ('2025-11-07 10:00:00', 123);


CREATE TABLE VoltMonth (
    volt_id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp_data DATETIME DEFAULT CURRENT_TIMESTAMP,
    voltM_value INT
);

INSERT into VoltMonth(`voltM_value`) VALUES
( 215),
( 746),
( 284),
(811),
( 862),
( 815),
( 83),
( 746),
( 118),
(115),
( 179),
(478),
( 733),
( 583),
( 158),
( 385),
( 630),
( 637),
( 10),
(938),
( 153),
(632),
(508),
(938),
( 640),
( 93),
(718),
( 335),
(76),
( 50);

CREATE TABLE VoltYear (
    volt_id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp_data DATETIME DEFAULT CURRENT_TIMESTAMP,
    voltY_value INT
);

INSERT into `VoltYear`(`voltY_value`) VALUES
( 201),
( 896),
( 133),
( 312),
( 712),
(394),
(142),
( 688),
(735),
( 319),
( 430),
(95);