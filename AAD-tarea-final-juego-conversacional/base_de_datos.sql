-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         8.0.31 - MySQL Community Server - GPL
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.3.0.6589
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para juego
CREATE DATABASE IF NOT EXISTS `juego` /*!40100 DEFAULT CHARACTER SET latin1 COLLATE latin1_spanish_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `juego`;

-- Volcando estructura para tabla juego.objeto
CREATE TABLE IF NOT EXISTS `objeto` (
  `idobjeto` int NOT NULL AUTO_INCREMENT,
  `nombreobjeto` varchar(40) CHARACTER SET latin1 COLLATE latin1_spanish_ci NOT NULL,
  `idsala` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`idobjeto`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

-- Volcando datos para la tabla juego.objeto: ~9 rows (aproximadamente)
DELETE FROM `objeto`;
INSERT INTO `objeto` (`idobjeto`, `nombreobjeto`, `idsala`) VALUES
  (1, 'mesa', 1),
  (2, 'candelabro', 1),
  (3, 'cuadro', 2),
  (4, 'llave', 2),
  (5, 'cofre', 2),
  (6, 'monedas', 2),
  (7, 'cuchillo', 3),
  (8, 'escudo', 3),
  (9, 'palanca', 4);

-- Volcando estructura para tabla juego.partidas_guardadas
CREATE TABLE IF NOT EXISTS `partidas_guardadas` (
  `jugador` varchar(40) CHARACTER SET latin1 COLLATE latin1_spanish_ci NOT NULL,
  `archivo` varchar(40) CHARACTER SET latin1 COLLATE latin1_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`jugador`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

-- Volcando datos para la tabla juego.partidas_guardadas: ~0 rows (aproximadamente)
DELETE FROM `partidas_guardadas`;

-- Volcando estructura para tabla juego.personaje
CREATE TABLE IF NOT EXISTS `personaje` (
  `idpersonaje` int NOT NULL,
  `idsala` int DEFAULT NULL,
  `nombrepersonaje` varchar(40) CHARACTER SET latin1 COLLATE latin1_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`idpersonaje`),
  KEY `idpersonaje` (`idpersonaje`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

-- Volcando datos para la tabla juego.personaje: ~2 rows (aproximadamente)
DELETE FROM `personaje`;
INSERT INTO `personaje` (`idpersonaje`, `idsala`, `nombrepersonaje`) VALUES
  (1, 3, 'guerrero'),
  (2, 4, 'tendero');

-- Volcando estructura para tabla juego.puntuaciones
CREATE TABLE IF NOT EXISTS `puntuaciones` (
  `idpartida` int NOT NULL AUTO_INCREMENT,
  `puntuacion` int NOT NULL DEFAULT '0',
  `jugador` varchar(40) CHARACTER SET latin1 COLLATE latin1_spanish_ci NOT NULL,
  PRIMARY KEY (`idpartida`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

-- Volcando datos para la tabla juego.puntuaciones: ~12 rows (aproximadamente)
DELETE FROM `puntuaciones`;

-- Volcando estructura para tabla juego.record
CREATE TABLE IF NOT EXISTS `record` (
  `idpartida` int NOT NULL AUTO_INCREMENT,
  `puntuacion` int NOT NULL DEFAULT '0',
  `jugador` varchar(40) CHARACTER SET latin1 COLLATE latin1_spanish_ci NOT NULL,
  PRIMARY KEY (`idpartida`) USING BTREE,
  CONSTRAINT `record_ibfk_1` FOREIGN KEY (`idpartida`) REFERENCES `puntuaciones` (`idpartida`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

-- Volcando datos para la tabla juego.record: ~1 rows (aproximadamente)
DELETE FROM `record`;

-- Volcando estructura para tabla juego.sala
CREATE TABLE IF NOT EXISTS `sala` (
  `idsala` int NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(1000) CHARACTER SET latin1 COLLATE latin1_spanish_ci NOT NULL DEFAULT '0',
  PRIMARY KEY (`idsala`),
  KEY `id` (`idsala`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

-- Volcando datos para la tabla juego.sala: ~5 rows (aproximadamente)
DELETE FROM `sala`;
INSERT INTO `sala` (`idsala`, `descripcion`) VALUES
  (1, 'Te encuentras en una enorme sala llena de columnas. No hay apenas luz, y el olor es nauseabundo. Te has tropezado con una mesa al entrar, mientras huías de algo que no has visto. Pero sabes que anda cerca. Mejor salir de aquí antes de descubrir qué es.'),
  (2, 'Has entrado en el salón principal de esta enorme fortaleza. Está lleno de estantes con armaduras de acero templado. Todos los yelmos lucen el emblema del rey. Parece que este sitio no ha sido pisado en siglos, y sin embargo todas las lámparas de aceite están encendidas. Distingues un esotérico cuadro colgado en un muro, un cofre en el muro opuesto y dos puertas al final.'),
  (3, 'Entras en una mazmorra llena de jaulas con esqueletos humanos. Conforme te adentras, el suelo de piedra da paso a un barro mojado de olor desagradable. Ves a un guerrero de la guardia real apoyado en un muro, y un cuchillo tirado en el suelo.'),
  (4, 'Al abrir la puerta reconoces un inconfundible olor a incienso. La habitación está iluminada por dos velas, y desde dentro te espía un tendero con los ojos afilados. Te pide que pases a su humilde tienda. En el mostrador hay una palanca con un precio de 90 monedas de oro.'),
  (5, 'Sales a lo que intuyes que es un vestíbulo, prácticamente vacío pero con las lámparas también iluminadas. Hay una puerta atrancada al fondo, y no te ves capaz de abrirla a patadas. ');

-- Volcando estructura para tabla juego.salida
CREATE TABLE IF NOT EXISTS `salida` (
  `idsalida` int NOT NULL AUTO_INCREMENT,
  `idsala` int NOT NULL DEFAULT '0',
  `salida` varchar(10) CHARACTER SET latin1 COLLATE latin1_spanish_ci NOT NULL DEFAULT '0',
  `idsalasalida` int DEFAULT NULL,
  PRIMARY KEY (`idsalida`),
  KEY `idsalida` (`idsalida`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

-- Volcando datos para la tabla juego.salida: ~9 rows (aproximadamente)
DELETE FROM `salida`;
INSERT INTO `salida` (`idsalida`, `idsala`, `salida`, `idsalasalida`) VALUES
  (1, 1, 'sur', 3),
  (2, 1, 'este', 2),
  (3, 2, 'este', 5),
  (4, 2, 'oeste', 1),
  (5, 2, 'sur', 4),
  (6, 3, 'norte', 1),
  (7, 4, 'norte', 2),
  (8, 5, 'este', 0),
  (9, 5, 'oeste', 2);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
