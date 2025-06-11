-- MySQL dump 10.13  Distrib 8.0.42, for Linux (x86_64)
--
-- Host: localhost    Database: club77
-- ------------------------------------------------------
-- Server version	8.0.42

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
-- Table structure for table `events`
--

DROP TABLE IF EXISTS `events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `events` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `event_date` date NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `webflow_id` varchar(255) DEFAULT NULL,
  `webflow_slug` varchar(255) DEFAULT NULL,
  `description` text,
  `artwork_url` varchar(500) DEFAULT NULL,
  `start_time` varchar(50) DEFAULT '10:00 PM',
  `end_time` varchar(50) DEFAULT '5:00 AM',
  `venue` varchar(255) DEFAULT '77 William St, Darlinghurst',
  `is_live` tinyint(1) NOT NULL DEFAULT '1',
  `webflow_published` tinyint(1) NOT NULL DEFAULT '0',
  `last_synced` datetime DEFAULT NULL,
  `muzeek_id` varchar(255) DEFAULT NULL,
  `muzeek_published` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `webflow_id` (`webflow_id`),
  UNIQUE KEY `muzeek_id` (`muzeek_id`),
  KEY `idx_events_webflow_id` (`webflow_id`),
  KEY `idx_events_is_live` (`is_live`),
  KEY `idx_events_muzeek_id` (`muzeek_id`),
  KEY `idx_events_muzeek_published` (`muzeek_published`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events`
--

LOCK TABLES `events` WRITE;
/*!40000 ALTER TABLE `events` DISABLE KEYS */;
INSERT INTO `events` VALUES (4,'Club 77 x Tempo Comodo: Dreems, Phil Smart','2025-05-29','2025-05-27 02:50:48','2025-05-27 03:00:03',NULL,NULL,'Free entry all night long.\n','https://muzeek-prod.nyc3.cdn.digitaloceanspaces.com/graphics/flyers/flyer_1030316652_1744853447.jpeg','22:00:00','03:00:00','Club 77',1,0,'2025-05-27 03:00:03','425015',1),(5,'Fridays at 77: Wavyrager, Yemi Sul','2025-05-30','2025-05-27 02:50:48','2025-05-27 03:00:03',NULL,NULL,'Free on guest list before 12am\n$15.00 After\n','https://muzeek-prod.nyc3.cdn.digitaloceanspaces.com/graphics/flyers/flyer_1692935843_1744684511.jpeg','22:00:00','05:00:00','Club 77',1,0,'2025-05-27 03:00:03','425016',1),(6,'Club 77: Phil Smart','2025-05-31','2025-05-27 02:50:48','2025-05-27 03:00:03',NULL,NULL,'Free on guest list before 12am\n$25.00 After\n','https://muzeek-prod.nyc3.cdn.digitaloceanspaces.com/graphics/flyers/flyer_1210786471_1744848808.jpg','22:00:00','05:00:00','Club 77',1,0,'2025-05-27 03:00:03','425026',1),(7,'Fridays at 77: Ayebatonye, Deepa','2025-06-06','2025-05-27 02:50:48','2025-05-27 03:00:03',NULL,NULL,'Free on guest list before 12am\n$15.00 After\n','https://muzeek-prod.nyc3.cdn.digitaloceanspaces.com/graphics/flyers/flyer_132779006_1746490968.jpeg','22:00:00','05:00:00','Club 77',1,0,'2025-05-27 03:00:03','438007',1),(8,'Club 77: Mazzacles, Kate Doherty & Aphasic','2025-06-07','2025-05-27 02:50:48','2025-05-27 03:00:03',NULL,NULL,'Free on guest list before 12am\n$25.00 After\n','https://muzeek-prod.nyc3.cdn.digitaloceanspaces.com/graphics/flyers/flyer_699341268_1746491636.jpg','22:00:00','05:00:00','Club 77',1,0,'2025-05-27 03:00:03','438011',1),(9,'Sundays at 77: Barney Kato & Simon Caldwell','2025-06-08','2025-05-27 02:50:48','2025-05-27 03:00:03',NULL,NULL,'Free on guest list before 12am\n$15.00 After\n','https://muzeek-prod.nyc3.cdn.digitaloceanspaces.com/graphics/flyers/flyer_641625644_1746491697.jpg','22:00:00','04:00:00','Club 77',1,0,'2025-05-27 03:00:03','438015',1),(10,'Fridays at 77: Ciara, Scruffs','2025-06-13','2025-05-27 02:50:48','2025-05-27 03:00:03',NULL,NULL,'Free on guest list before 12am\n$15.00 After\n','https://muzeek-prod.nyc3.cdn.digitaloceanspaces.com/graphics/flyers/flyer_820206029_1747100644.jpeg','22:00:00','05:00:00','Club 77',1,0,'2025-05-27 03:00:03','444020',1),(11,'Club 77: Reenie, Goat Spokesperson','2025-06-14','2025-05-27 02:50:48','2025-05-27 03:00:03',NULL,NULL,'Free on guest list before 12am\n$25.00 After\n','https://muzeek-prod.nyc3.cdn.digitaloceanspaces.com/graphics/flyers/flyer_1672217449_1747102795.jpeg','22:00:00','05:00:00','Club 77',1,0,'2025-05-27 03:00:03','438016',1),(12,'Fridays at 77: Wavyrager, halalbutch','2025-06-20','2025-05-27 02:50:48','2025-05-27 03:00:03',NULL,NULL,'Free on guest list before 12am\n$15.00 After\n','https://muzeek-prod.nyc3.cdn.digitaloceanspaces.com/graphics/flyers/flyer_868873842_1747702887.jpeg','22:00:00','05:00:00','Club 77',1,0,'2025-05-27 03:00:03','444013',1),(13,'Club 77: Mike Who & Daniel Lupica','2025-06-21','2025-05-27 02:50:48','2025-05-27 03:00:03',NULL,NULL,'Free on guest list before 12am\n$25.00 After\n','https://muzeek-prod.nyc3.cdn.digitaloceanspaces.com/graphics/flyers/flyer_969978570_1747707305.jpeg','22:00:00','05:00:00','Club 77',1,0,'2025-05-27 03:00:03','438017',1),(14,'Fridays at 77: Jhassic, Kiminza','2025-06-27','2025-05-27 02:50:48','2025-05-27 03:00:03',NULL,NULL,'Free on guest list before 12am\n$15.00 After\n','https://muzeek-prod.nyc3.cdn.digitaloceanspaces.com/graphics/flyers/flyer_838739147_1748309896.jpeg','22:00:00','01:00:00','Club 77',1,0,'2025-05-27 03:00:03','444544',1);
/*!40000 ALTER TABLE `events` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-27  3:04:26
