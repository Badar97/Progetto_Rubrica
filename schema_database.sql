CREATE DATABASE IF NOT EXISTS rubrica;

USE rubrica;

CREATE TABLE IF NOT EXISTS persone (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255),
    cognome VARCHAR(255),
    indirizzo VARCHAR(255),
    telefono VARCHAR(20),
    eta INT
);
