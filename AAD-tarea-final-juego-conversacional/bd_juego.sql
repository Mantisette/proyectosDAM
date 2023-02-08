-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         8.0.31 - MySQL Community Server - GPL
-- SO del servidor:              macos12
-- HeidiSQL Versión:             12.1.0.6537
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
DROP DATABASE IF EXISTS `juego`;
CREATE DATABASE IF NOT EXISTS `juego` /*!40100 DEFAULT CHARACTER SET latin1 COLLATE latin1_spanish_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `juego`;

-- Volcando estructura para tabla juego.objeto
DROP TABLE IF EXISTS `objeto`;
CREATE TABLE IF NOT EXISTS `objeto` (
  `idobjeto` int NOT NULL AUTO_INCREMENT,
  `idsala` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`idobjeto`),
  KEY `idobjeto` (`idobjeto`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

-- Volcando datos para la tabla juego.objeto: ~0 rows (aproximadamente)
DELETE FROM `objeto`;
INSERT INTO `objeto` (`idobjeto`, `idsala`) VALUES
	(1, 2),
	(2, 2),
	(3, 1),
	(4, 3),
	(5, 4),
	(6, 3),
	(7, 1),
	(8, 4),
	(9, 2);

-- Volcando estructura para tabla juego.personaje
DROP TABLE IF EXISTS `personaje`;
CREATE TABLE IF NOT EXISTS `personaje` (
  `idpersonaje` int NOT NULL,
  `idsala` int DEFAULT NULL,
  PRIMARY KEY (`idpersonaje`),
  KEY `idpersonaje` (`idpersonaje`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

-- Volcando datos para la tabla juego.personaje: ~0 rows (aproximadamente)
DELETE FROM `personaje`;
INSERT INTO `personaje` (`idpersonaje`, `idsala`) VALUES
	(1, 3),
	(2, 4);

-- Volcando estructura para tabla juego.sala
DROP TABLE IF EXISTS `sala`;
CREATE TABLE IF NOT EXISTS `sala` (
  `idsala` int NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(1000) COLLATE latin1_spanish_ci NOT NULL DEFAULT '0',
  PRIMARY KEY (`idsala`),
  KEY `id` (`idsala`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

-- Volcando datos para la tabla juego.sala: ~0 rows (aproximadamente)
DELETE FROM `sala`;
INSERT INTO `sala` (`idsala`, `descripcion`) VALUES
	(1, 'Te encuentras en una enorme sala llena de columnas , no hay apenas luz, el olor es desagradable, algo anda cerca'),
	(2, 'Has entrado en salon, de esta enorme fortaleza, es amplio y muy luminoso, a lo lejo se aprecia un par de puertas'),
	(3, 'Estas en una mazmorra llena de esqueletos de antiguos inquilinos, el suelo es tierra y parece estar mojado'),
	(4, 'Bienvenido a la tienda de esta fortaleza, el tendero estara encantado de hacer tratos contigo'),
	(5, 'Has llegado a una habitacion , quizas sea el fin de todo o comiezo de algo nuevo, se ve una puerta al final, pero parece cerrada');

-- Volcando estructura para tabla juego.salida
DROP TABLE IF EXISTS `salida`;
CREATE TABLE IF NOT EXISTS `salida` (
  `idsalida` int NOT NULL AUTO_INCREMENT,
  `idsala` int NOT NULL DEFAULT '0',
  `salida` varchar(10) COLLATE latin1_spanish_ci NOT NULL DEFAULT '0',
  `idsalasalida` int DEFAULT NULL,
  PRIMARY KEY (`idsalida`),
  KEY `idsalida` (`idsalida`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

-- Volcando datos para la tabla juego.salida: ~0 rows (aproximadamente)
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
