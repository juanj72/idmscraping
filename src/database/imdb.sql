-- MySQL dump 10.13  Distrib 8.0.42, for Linux (x86_64)
--
-- Host: 192.168.10.27    Database: imdb
-- ------------------------------------------------------
-- Server version	9.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `imdb`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `imdb` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `imdb`;

--
-- Table structure for table `actores`
--

DROP TABLE IF EXISTS `actores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `actores` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=8603 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `actores`
--

LOCK TABLES `actores` WRITE;
/*!40000 ALTER TABLE `actores` DISABLE KEYS */;
/*!40000 ALTER TABLE `actores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `desviacion_estandar_calificaciones_anio`
--

DROP TABLE IF EXISTS `desviacion_estandar_calificaciones_anio`;
/*!50001 DROP VIEW IF EXISTS `desviacion_estandar_calificaciones_anio`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `desviacion_estandar_calificaciones_anio` AS SELECT 
 1 AS `anio`,
 1 AS `cantidad_peliculas`,
 1 AS `promedio_calificacion`,
 1 AS `desviacion_estandar`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `metascore_normalizado`
--

DROP TABLE IF EXISTS `metascore_normalizado`;
/*!50001 DROP VIEW IF EXISTS `metascore_normalizado`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `metascore_normalizado` AS SELECT 
 1 AS `titulo`,
 1 AS `anio`,
 1 AS `calificacion`,
 1 AS `metascore`,
 1 AS `metascore_normalizado`,
 1 AS `diferencia_porcentual`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `peliculas`
--

DROP TABLE IF EXISTS `peliculas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `peliculas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `titulo` varchar(255) NOT NULL,
  `anio` int NOT NULL,
  `calificacion` int DEFAULT NULL,
  `duracion` float DEFAULT NULL,
  `metascore` float DEFAULT NULL,
  `url` varchar(512) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `url` (`url`)
) ENGINE=InnoDB AUTO_INCREMENT=4114 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `peliculas`
--

LOCK TABLES `peliculas` WRITE;
/*!40000 ALTER TABLE `peliculas` DISABLE KEYS */;
/*!40000 ALTER TABLE `peliculas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `peliculas_actores`
--

DROP TABLE IF EXISTS `peliculas_actores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `peliculas_actores` (
  `pelicula_id` int NOT NULL,
  `actor_id` int NOT NULL,
  PRIMARY KEY (`pelicula_id`,`actor_id`),
  KEY `actor_id` (`actor_id`),
  CONSTRAINT `peliculas_actores_ibfk_1` FOREIGN KEY (`pelicula_id`) REFERENCES `peliculas` (`id`) ON DELETE CASCADE,
  CONSTRAINT `peliculas_actores_ibfk_2` FOREIGN KEY (`actor_id`) REFERENCES `actores` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `peliculas_actores`
--

LOCK TABLES `peliculas_actores` WRITE;
/*!40000 ALTER TABLE `peliculas_actores` DISABLE KEYS */;
/*!40000 ALTER TABLE `peliculas_actores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `peliculas_mayor_promedio_duracion_decada`
--

DROP TABLE IF EXISTS `peliculas_mayor_promedio_duracion_decada`;
/*!50001 DROP VIEW IF EXISTS `peliculas_mayor_promedio_duracion_decada`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `peliculas_mayor_promedio_duracion_decada` AS SELECT 
 1 AS `decada`,
 1 AS `titulo`,
 1 AS `anio`,
 1 AS `duracion`*/;
SET character_set_client = @saved_cs_client;

--
-- Dumping events for database 'imdb'
--

--
-- Dumping routines for database 'imdb'
--

--
-- Current Database: `imdb`
--

USE `imdb`;

--
-- Final view structure for view `desviacion_estandar_calificaciones_anio`
--

/*!50001 DROP VIEW IF EXISTS `desviacion_estandar_calificaciones_anio`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `desviacion_estandar_calificaciones_anio` AS select `peliculas`.`anio` AS `anio`,count(0) AS `cantidad_peliculas`,avg(`peliculas`.`metascore`) AS `promedio_calificacion`,stddev_samp(`peliculas`.`metascore`) AS `desviacion_estandar` from `peliculas` group by `peliculas`.`anio` order by `peliculas`.`anio` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `metascore_normalizado`
--

/*!50001 DROP VIEW IF EXISTS `metascore_normalizado`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `metascore_normalizado` AS select `peliculas`.`titulo` AS `titulo`,`peliculas`.`anio` AS `anio`,`peliculas`.`calificacion` AS `calificacion`,`peliculas`.`metascore` AS `metascore`,round((`peliculas`.`metascore` / 10),2) AS `metascore_normalizado`,round(((abs((`peliculas`.`calificacion` - (`peliculas`.`metascore` / 10))) / `peliculas`.`calificacion`) * 100),2) AS `diferencia_porcentual` from `peliculas` where ((`peliculas`.`calificacion` is not null) and (`peliculas`.`metascore` is not null) and ((abs((`peliculas`.`calificacion` - (`peliculas`.`metascore` / 10))) / `peliculas`.`calificacion`) > 0.20)) order by round(((abs((`peliculas`.`calificacion` - (`peliculas`.`metascore` / 10))) / `peliculas`.`calificacion`) * 100),2) desc */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `peliculas_mayor_promedio_duracion_decada`
--

/*!50001 DROP VIEW IF EXISTS `peliculas_mayor_promedio_duracion_decada`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `peliculas_mayor_promedio_duracion_decada` AS with `peliculas_con_ranking` as (select (floor((`peliculas`.`anio` / 10)) * 10) AS `decada`,`peliculas`.`titulo` AS `titulo`,`peliculas`.`anio` AS `anio`,`peliculas`.`duracion` AS `duracion`,row_number() OVER (PARTITION BY (floor((`peliculas`.`anio` / 10)) * 10) ORDER BY `peliculas`.`duracion` desc )  AS `rk` from `peliculas`) select `peliculas_con_ranking`.`decada` AS `decada`,`peliculas_con_ranking`.`titulo` AS `titulo`,`peliculas_con_ranking`.`anio` AS `anio`,`peliculas_con_ranking`.`duracion` AS `duracion` from `peliculas_con_ranking` where (`peliculas_con_ranking`.`rk` <= 5) order by `peliculas_con_ranking`.`decada`,`peliculas_con_ranking`.`rk` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-27  1:21:57
