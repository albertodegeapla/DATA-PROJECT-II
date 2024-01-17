-- DROP TABLE IF EXISTS
DROP TABLE IF EXISTS personas CASCADE;
DROP TABLE IF EXISTS plazas_disponibles CASCADE;
DROP TABLE IF EXISTS viajes_asignados CASCADE;
DROP TABLE IF EXISTS lista_espera CASCADE;

-- TABLA PERSONAS

CREATE TABLE IF NOT EXISTS personas (
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
    Estado_civil VARCHAR(50) NOT NULL,
    Acompanamiento_pareja BOOLEAN NOT NULL,
    Hijo_discapacidad BOOLEAN NOT NULL,
    Discapacidad BOOLEAN NOT NULL,
    Tipo_discapacidad VARCHAR(50),
    Grado_discapacidad INT,
    Numero_participaciones INT,
    Renta INT NOT NULL,
    Personas_dependientes INT,
    Pension VARCHAR(50),
    Obras_sociales VARCHAR(50) NOT NULL,
    Vive_solo BOOLEAN NOT NULL,
    Preferencia_1 VARCHAR(50),
    Preferencia_2 VARCHAR(50),
    Fecha_1 VARCHAR(50),
    Fecha_2 VARCHAR(50),
    Fecha_3 VARCHAR(50)
);

-- TABLA PLAZAS_DISPONIBLES

CREATE TABLE IF NOT EXISTS plazas_disponibles (
    id_plaza SERIAL PRIMARY KEY,
    Ciudad VARCHAR(50) NOT NULL,
    Mes VARCHAR(50) NOT NULL,
    Hotel VARCHAR(50) NOT NULL,
    Estrellas_hotel INT NOT NULL,
    Tipo_exp VARCHAR(50) NOT NULL,
    Fecha_viaje DATE NOT NULL,
    Num_plazas INT NOT NULL
);

-- TABLA VIAJES_ASIGNADOS

CREATE TABLE IF NOT EXISTS viajes_asignados (
    id_viaje SERIAL PRIMARY KEY,
    id_persona INT NOT NULL,
    Nombre VARCHAR(50) NOT NULL,
    Primer_apellido VARCHAR(50) NOT NULL,
    Segundo_apellido VARCHAR(50) NOT NULL,
    DNI VARCHAR(50) NOT NULL,
    Ciudad VARCHAR(50) NOT NULL,
    tipo_exp VARCHAR(50) NOT NULL,
    Hotel VARCHAR(50) NOT NULL,
    Mes VARCHAR(50) NOT NULL,
    Fecha_viaje DATE NOT NULL,
    Valoracion INT NOT NULL
);

-- TABLA LISTA_ESPERA

CREATE TABLE IF NOT EXISTS lista_espera (
    id_lista_espera SERIAL PRIMARY KEY,
    id_persona INT NOT NULL,
    Nombre VARCHAR(50) NOT NULL,
    Primer_apellido VARCHAR(50) NOT NULL,
    Segundo_apellido VARCHAR(50) NOT NULL,
    DNI VARCHAR(50) NOT NULL,
    Valoracion INT NOT NULL
);






