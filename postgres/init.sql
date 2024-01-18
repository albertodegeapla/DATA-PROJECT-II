-- DROP TABLE IF EXISTS
DROP TABLE IF EXISTS persona CASCADE;
DROP TABLE IF EXISTS coche CASCADE;
DROP TABLE IF EXISTS ruta CASCADE;
DROP TABLE IF EXISTS cartera CASCADE;

-- TABLA PERSONAS

CREATE TABLE IF NOT EXISTS persona (
    id_persona SERIAL PRIMARY KEY,
    Nombre VARCHAR(50) NOT NULL,
    Primer_apellido VARCHAR(50) NOT NULL,
    Segundo_apellido VARCHAR(50) NOT NULL,
    Sexo VARCHAR(50) NOT NULL,
    Nacionalidad VARCHAR(1000) NOT NULL,
    DNI VARCHAR(50) NOT NULL,
    Telefono VARCHAR(15) NOT NULL,
    Pais_residencia VARCHAR(10000) NOT NULL,
    Fecha_nacimiento DATE NOT NULL,
    Edad INT NOT NULL,
    Provincia VARCHAR(50) NOT NULL,
    id_conductor INT NOT NULL
);

-- TABLA coche

CREATE TABLE IF NOT EXISTS coche (
    id_coche SERIAL PRIMARY KEY,
    num_matricula INT NOT NULL,
    marca VARCHAR(50) NOT NULL,
    id_conductor INT NOT NULL,
    plazas INT NOT NULL,
    color VARCHAR(50) NOT NULL,
    letras_matricula VARCHAR(50) NOT NULL,
    kilometraje INT NOT NULL
);

-- TABLA RUTA

CREATE TABLE IF NOT EXISTS ruta (
    id_coche SERIAL PRIMARY KEY,
    id_conductor INT NOT NULL,
    salida VARCHAR(1000) NOT NULL,
    destino VARCHAR(1000) NOT NULL,
    fecha_viaje DATE NOT NULL,
    precio INT NOT NULL,
    km_recorridos INT NOT NULL
);

-- TABLA cartera

CREATE TABLE IF NOT EXISTS cartera (
    id_persona SERIAL PRIMARY KEY,
    id_conductor INT NOT NULL,
    cartera INT NOT NULL
);