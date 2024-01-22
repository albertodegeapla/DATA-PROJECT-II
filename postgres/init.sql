-- DROP TABLE IF EXISTS
DROP TABLE IF EXISTS persona CASCADE;
DROP TABLE IF EXISTS coche CASCADE;

-- TABLA PERSONAS

CREATE TABLE IF NOT EXISTS persona (
    id_persona SERIAL PRIMARY KEY,
    Nombre VARCHAR(50) NOT NULL,
    Primer_apellido VARCHAR(50) NOT NULL,
    Segundo_apellido VARCHAR(50) NOT NULL,
    Cartera INT NOT NULL
);

-- TABLA coche

CREATE TABLE IF NOT EXISTS coche (
    id_coche SERIAL PRIMARY KEY,
    id_persona INT NOT NULL,
    Num_matricula INT NOT NULL,
    Letras_matricula VARCHAR(50) NOT NULL,
    Marca VARCHAR(50) NOT NULL,
    Plazas INT NOT NULL,
    KM_precio INT NOT NULL
);